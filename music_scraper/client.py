import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from dateutil.relativedelta import *

from typing import Set
from bs4 import Tag


class MusicScraper():
    def __init__(self):
        # Billboard URLS
        self.billboard_base_url = 'https://www.billboard.com'

        self.artist_charts = self.billboard_base_url + '/charts/artist-100'

    def get_top_artists_names(self, last_x_weeks=1) -> Set[str]:
        """Get all the names of the artists who've reached Billboard's Artist 100 list in the last X weeks.

        Arguments:
        ----------
        last_x_weeks {int} -- The number of weeks before the current date to grab the artists.

        Returns:
        --------
        Set[str] -- Set containing artist names.
        """

        # Initialize the top artists names list.
        top_artists_names = set()

        # Get today's date in ISO Format
        current_date: datetime = datetime.now()

        # Grab the top artists from the last X weeks.
        for week in range(last_x_weeks):

            # Get the target date.
            target_date: datetime = current_date + relativedelta(
                weeks=-week
            )

            # Construct endpoint URL.
            full_url = self.artist_charts + '/{date}'.format(
                date=target_date.strftime('%Y-%m-%d')
            )

            # Grab the response.
            response = requests.get(url=full_url)
            print('URL REQUESTED: {url}'.format(url=full_url))

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
