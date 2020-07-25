import unittest
from unittest import TestCase

from music_scraper.client import MusicScraper


class MusicScraperTester(TestCase):

    def setUp(self) -> None:

        self.music_scraper = MusicScraper()

    def test_create_instance_of_music_scraper(self):
        """Can create instance of MusicScraper class."""

        self.assertIsInstance(self.music_scraper, MusicScraper)


if __name__ == '__main__':
    unittest.main()
