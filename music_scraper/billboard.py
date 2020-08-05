from pprint import pprint
import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from dateutil.relativedelta import *

from typing import Set
from typing import List
from bs4 import Tag


class BillboardScraper():
    def __init__(self):
        # Billboard URLs
        self._billboard_base_url = 'https://www.billboard.com'
        self._artist_charts = self._billboard_base_url + '/charts/artist-100'

    def get_top_artists_names(self, last_x_weeks=2) -> Set[str]:
        """Get all the names of the artists who've reached Billboard's Artist 100 list in the last X months.

        Arguments:
        ----------
        last_x_weeks {int} -- The number of weeks to go back on the charts (Default: 2)

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
