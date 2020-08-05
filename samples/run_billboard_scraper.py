from pprint import pprint

from music_scraper.billboard import BillboardScraper

# Initialize the Billboard scraper.
billboard_scraper = BillboardScraper()

# Grab the top artists names from the last 2 weeks
top_artists_names = billboard_scraper.get_top_artists_names(
    last_x_weeks=2
)
pprint(top_artists_names)

print('# of top artists: {}'.format(len(top_artists_names)))
