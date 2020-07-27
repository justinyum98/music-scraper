import base64
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from dateutil.relativedelta import *

from music_scraper.spotify_parser import SpotifyParser

from typing import Set
from bs4 import Tag


class MusicScraper():
    def __init__(self):
        # Billboard URLs
        self._billboard_base_url = 'https://www.billboard.com'
        self._artist_charts = self._billboard_base_url + '/charts/artist-100'

        # Spotify Parser
        self._spotify_parser = SpotifyParser()

        # Spotify URLs
        self._spotify_base_url = 'https://api.spotify.com/v1'
        self._search_endpoint = self._spotify_base_url + '/search'
        self._get_artist_endpoint = self._spotify_base_url + '/artists'

        # Spotify Auth URLs
        self._spotify_auth_base_url = 'https://accounts.spotify.com/api'
        self._authenticate_endpoint = self._spotify_auth_base_url + '/token'

        # Spotify Client Credentials
        self._spotify_client_id = 'a53d884eae824d73a4471a68e91dd480'
        self._spotify_client_secret = '8985ff9b2b18428cbc564b85df8579cf'

        # Authenticate the client.
        self._spotify_access_token = ''
        self._authenticate_client()

    def _authenticate_client(self) -> None:
        # Base64 encode the client credentials
        auth_str = bytes('{client_id}:{client_secret}'.format(
            client_id=self._spotify_client_id,
            client_secret=self._spotify_client_secret
        ), 'utf-8')
        b64_auth_str = base64.b64encode(auth_str).decode('utf-8')

        # Grab the response.
        response = requests.post(
            url=self._authenticate_endpoint,
            data={
                'grant_type': 'client_credentials'
            },
            headers={
                'Authorization': 'Basic {}'.format(b64_auth_str)
            }
        )
        print('URL REQUESTED: {}'.format(response.url))

        if response.ok:
            # Store the access token.
            response_data = response.json()
            self._spotify_access_token = response_data['access_token']
        else:
            print('Error {}: {}'.format(response.status_code, response.text))

    def get_top_artists_names(self, last_x_weeks=1) -> Set[str]:
        """Get all the names of the artists who've reached Billboard's Artist 100 list in the last X months.

        Returns:
        --------
        Set[str] -- Set containing artist names.
        """

        # Initialize the top artists names list.
        top_artists_names = set()

        # Get today's date in ISO Format
        current_date: datetime = datetime.now()

        # Grab the top artists.
        for week in range(last_x_weeks):

            # Get the target date.
            target_date: datetime = current_date + relativedelta(
                weeks=-week
            )

            # Construct endpoint URL.
            full_url = self._artist_charts + '/{date}'.format(
                date=target_date.strftime('%Y-%m-%d')
            )

            # Grab the response.
            response = requests.get(url=full_url)
            print('URL REQUESTED: {}'.format(response.url))

            # Parse the content.
            soup = BeautifulSoup(response.content, 'html.parser')

            # Grab the list of artist details.
            artist_details_list: List[Tag] = soup.find_all(
                name='div',
                attrs={'class': 'chart-list-item'}
            )

            # Add the artist name to the set.
            for artist_detail in artist_details_list:
                top_artists_names.add(artist_detail['data-title'])

        return top_artists_names

    def get_artists_spotify_ids(self, artist_names: Set[str]) -> dict:
        """Given a set of artists' names, return a dictionary of artists and their Spotify IDs.

        https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-search

        Arguments:
        ----------
        artist_names {Set[str]} -- A set containing artist names.

        Returns:
        --------
        dict -- Dictionary with the keys being the artist's name and the values being their Spotify IDs.
        """

        # Initialize the artists dictionary
        artists_spotify_ids = {}

        # Iterate through the artist names.
        for artist_name in artist_names:

            # Query for the artist in Spotify.
            # Make artist name URL safe.
            url_safe_artist_name = artist_name.replace(' ', '+')

            # Grab the response
            response = requests.get(
                url=self._search_endpoint,
                params={
                    'q': url_safe_artist_name,
                    'type': 'artist'
                },
                headers={
                    'Authorization': 'Bearer {token}'.format(token=self._spotify_access_token)
                }
            )
            print('URL REQUESTED: {}'.format(response.url))

            if response.ok:
                # Grab the response data.
                response_data = response.json()

                # Grab the list of artist matches.
                artist_list = response_data['artists']['items']

                # Check if list isn't empty.
                if artist_list:
                    # Get the first artist's Spotify ID.
                    artist_spotify_id = artist_list[0]['id']

                    # Store the first artist's Spotify ID.
                    artists_spotify_ids[artist_name] = artist_spotify_id
                else:
                    print('Query for {} is empty.'.format(artist_name))
            else:
                print('Error {}: {}'.format(response.status_code, response.text))

        return artists_spotify_ids

    def get_artist_by_id(self, spotify_id: str) -> dict:
        """Given an artist's Spotify ID, get the artist's data.

        https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-artist

        Arguments:
        ----------
        spotify_id {str} -- The artist's Spotify ID

        Returns:
        --------
        dict -- A dictionary containing the artist object.
        """

        # Attach ID to URL.
        full_url = self._get_artist_endpoint + '/{}'.format(spotify_id)

        # Grab the response
        response = requests.get(
            url=full_url,
            headers={
                'Authorization': 'Bearer {}'.format(self._spotify_access_token)
            }
        )

        if response.ok:
            # Grab the response data.
            response_data = response.json()

            # Parse the artist data.
            artist_data = self._spotify_parser.parse_artist_data(
                response_data=response_data
            )

            return artist_data
        else:
            print('Error {}: {}'.format(response.status_code, response.text))
