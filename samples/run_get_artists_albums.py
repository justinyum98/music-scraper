from pprint import pprint
import json
from music_scraper.client import MusicScraper

# Initialize the client.
music_scraper = MusicScraper()

# Load the artist names.
with open(file=r'samples/responses/spotify_artist_ids.jsonc', mode='r') as spotify_artist_ids_file:
    spotify_artist_ids = json.load(fp=spotify_artist_ids_file)

# Grab the artists data.
artist_data_list = []

for artist_name in spotify_artist_ids:

    # Grab the artist Spotify ID.
    artist_spotify_id = spotify_artist_ids[artist_name]

    # Grab the artist data.
    artist_data = music_scraper.get_artist_data_by_id(
        spotify_id=artist_spotify_id
    )

    # Store the artist data
    artist_data_list.append(artist_data)

pprint(artist_data_list)

# Save the artists data.
with open('samples/responses/artists_data.jsonc', 'w+') as artists_data_file:
    json.dump(obj=artist_data_list, fp=artists_data_file, indent=2)
