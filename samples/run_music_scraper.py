from pprint import pprint
import json

from music_scraper.client import MusicScraper

# Initialize the music scraper.
music_scraper = MusicScraper()

# Grab the top artists names from the last 6 weeks
top_artists_names = music_scraper.get_top_artists_names(6)
pprint(top_artists_names)

# Grab all their Spotify IDs
artists_spotify_ids = music_scraper.get_artists_spotify_ids(
    artist_names=top_artists_names
)
pprint(artists_spotify_ids)

print('# of top artists: {}'.format(len(top_artists_names)))
print('# of spotify IDs: {}'.format(len(artists_spotify_ids.keys())))

# Save the Spotify IDs.
with open('samples/responses/spotify_artist_ids.jsonc', 'w+') as spotify_artist_ids_file:
    json.dump(obj=artists_spotify_ids, fp=spotify_artist_ids_file, indent=2)
