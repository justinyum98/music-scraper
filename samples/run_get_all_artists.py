"""
Script that,
given a set containing unique Spotify IDs,
returns a set containing the original set + 'relevant' artist IDs.
'Relevant' being:
- Featured in tracks
- Co-artist on albums
- Spotify's recommended related artists.

This script utilizes recursion.
[TBD]

(Pseudocode)

for top_artist_name in top_artist_names:
    
    # Search/query for artist by name:


print result
"""
import json
from pprint import pprint
import requests

from typing import Set
from typing import List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from music_scraper.billboard import BillboardScraper

##### GET BILLBOARD TOP ARTIST NAMES #####
# Initialize the Billboard scraper.
billboard_scraper = BillboardScraper()

# Grab the top artists names from the last 2 weeks
top_artists_names = billboard_scraper.get_top_artists_names(
    last_x_weeks=2
)
pprint(top_artists_names)


##### GET BILLBOARD TOP ARTIST SPOTIFY IDS #####
# Initialize Spotify Client with Client Credentials Flow
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# Create a set of the Billboard artists' Spotify IDs.
spotify_ids: Set[str] = set()

for top_artist_name in top_artists_names:

    # Make query URL-safe (replace space with +).
    query = top_artist_name.replace(' ', '+')

    # Search for the artist by name.
    search_result: List[dict] = sp.search(
        q=query,
        type='artist'
    )['artists']['items']

    # Check if search result is not empty.
    if search_result:
        # If so, grab the first result's Spotify ID.
        spotify_ids.add(search_result[0]['id'])

pprint(spotify_ids)


##### GET ALL RELEVANT ARTIST SPOTIFY IDS #####
def get_relevant_artist_ids(artist_id: str, added_artist_ids: Set[str]) -> Set[str]:
    """Given an artist's Spotify ID, get all 'relevant' artists' Spotify IDs.
    'Relevant' being:
    - Co-artist on albums/singles
    - Featured in tracks
    - Spotify's recommended related artists.

    Args:
        artist_id (str): Spotify ID of artist.

    Returns:
        Set[str]: Set containing all relevant artist Spotify IDs.
    """

    added_artist_ids_copy = added_artist_ids.copy()

    # Grab the artist's albums
    artist_albums: List[dict] = sp.artist_albums(
        artist_id=artist_id,
        album_type='album',
        limit=50
    )['items']

    # Iterate through artist's albums.
    for artist_album in artist_albums:
        # Grab the album's artists.
        album_artists: List[dict] = artist_album['artists']

        # Iterate through the album's artists.
        for album_artist in album_artists:
            # If the id is not recorded...
            if album_artist['id'] not in added_artist_ids_copy:
                # Add the id.
                added_artist_ids_copy.add(album_artist['id'])
                # Grab the artist's relevant artists, get the union, update the added artist ids.
                added_artist_ids_copy = added_artist_ids_copy.union(
                    get_relevant_artist_ids(
                        artist_id=album_artist['id'],
                        added_artist_ids=added_artist_ids_copy
                    )
                )

        # Grab the album's tracks.
        album_tracks: List[dict] = sp.album_tracks(
            album_id=artist_album['id']
        )['items']

        # Iterate through album's tracks.
        for album_track in album_tracks:
            # Grab the track's artists.
            track_artists: List[dict] = album_track['artists']

            # Iterate through the track's artists.
            for track_artist in track_artists:
                # If the id is not recorded...
                if track_artist['id'] not in added_artist_ids_copy:
                    # Add the id.
                    added_artist_ids_copy.add(track_artist['id'])
                    # Grab the artist's relevant artists, get the union, update the added artist ids.
                    added_artist_ids_copy = added_artist_ids_copy.union(
                        get_relevant_artist_ids(
                            artist_id=track_artist['id'],
                            added_artist_ids=added_artist_ids_copy
                        )
                    )

    # Grab the artist's singles.
    artist_singles: List[dict] = sp.artist_albums(
        artist_id=artist_id,
        album_type='single',
        limit=50
    )['items']

    # Iterate through artist's singles.
    for artist_single in artist_singles:
        # Grab the single's artists.
        single_artists: List[dict] = artist_single['artists']

        # Iterate through the single's artists.
        for single_artist in single_artists:
            # If the id is not recorded...
            if single_artist['id'] not in added_artist_ids_copy:
                # Add the id
                added_artist_ids_copy.add(single_artist['id'])
                # Grab the artist's relevant artists, get the union, update the added artist ids.
                added_artist_ids_copy = added_artist_ids_copy.union(
                    get_relevant_artist_ids(
                        artist_id=single_artist['id'],
                        added_artist_ids=added_artist_ids_copy
                    )
                )

        # Grab the single's tracks.
        single_tracks: List[dict] = sp.album_tracks(
            album_id=artist_single['id']
        )['items']

        # Iterate through the single's tracks.
        for single_track in single_tracks:
            # Grab the track's artists.
            track_artists: List[dict] = single_track['artists']
            
            # Iterate through the track's artists.
            for track_artist in track_artists:
                # If the id is not recorded...
                if track_artist['id'] not in added_artist_ids_copy:
                    # Add the id.
                    added_artist_ids_copy.add(track_artist['id'])
                    # Grab the artist's relevant artists, get the union, update the added artist ids.
                    added_artist_ids_copy = added_artist_ids_copy.union(
                        get_relevant_artist_ids(
                            artist_id=track_artist['id'],
                            added_artist_ids=added_artist_ids_copy
                        )
                    )


    # Grab an artist's related artists.
    related_artists: List[dict] = sp.artist_related_artists(
        artist_id=artist_id
    )['artists']

    # Iterate through the artist's related artists.
    for related_artist in related_artists:
        # If the id is not recorded...
        if related_artist['id'] not in added_artist_ids_copy:
            # Add the id.
            added_artist_ids_copy.add(related_artist['id'])
            # Grab the artist's relevant artists, get the union, update the added artist ids.
            added_artist_ids_copy = added_artist_ids_copy.union(
                get_relevant_artist_ids(
                    artist_id=related_artist['id'],
                    added_artist_ids=added_artist_ids_copy
                )
            )

    # Return the result.
    return added_artist_ids_copy


all_spotify_ids = spotify_ids.copy()

for artist_id in spotify_ids:

    added_spotify_ids = all_spotify_ids.copy()

    # Grab relevant artist ids.
    relevant_artist_ids = get_relevant_artist_ids(
        artist_id=artist_id,
        added_artist_ids=added_spotify_ids
    )

    # Get the union of the two sets.
    all_spotify_ids = all_spotify_ids.union(relevant_artist_ids)
