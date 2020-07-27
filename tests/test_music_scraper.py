import unittest
from unittest import TestCase

from music_scraper.client import MusicScraper

from typing import Set


class MusicScraperTester(TestCase):

    def setUp(self) -> None:

        self.music_scraper = MusicScraper()

    def test_create_instance_of_music_scraper(self):
        """Can create instance of MusicScraper class."""

        self.assertIsInstance(self.music_scraper, MusicScraper)

    def test_get_top_artists_names(self):
        """Can get all the names of the artists who've reached Billboard's Artist 100 list in the last X weeks."""

        top_artists_list: Set[str] = self.music_scraper.get_top_artists_names(2)

        self.assertIsNotNone(top_artists_list)

    def test_get_artists_spotify_ids(self):
        """Given multiple artist names, can get the artists' respective Spotify IDs."""

        # Get the artists names.
        top_artists_list: Set[str] = self.music_scraper.get_top_artists_names(2)

        # Grab the artists' Spotify IDs.
        artists_spotify_ids: dict = self.music_scraper.get_artists_spotify_ids(
            artist_names=top_artists_list
        )

        self.assertIsNotNone(artists_spotify_ids)

if __name__ == '__main__':
    unittest.main()
