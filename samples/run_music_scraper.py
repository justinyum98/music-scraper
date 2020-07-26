from pprint import pprint

from music_scraper.client import MusicScraper

# Initialize the music scraper.
music_scraper = MusicScraper()

# Grab the top artists names in the last 5 weeks.
top_artists_names = music_scraper.get_top_artists_names(
    last_x_weeks=5
)
pprint(top_artists_names)
