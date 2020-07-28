from pprint import pprint
import json

from music_scraper.client import MusicScraper

# Initialize the music scraper.
music_scraper = MusicScraper()

# Grab the top artists names from the last 2 weeks
top_artists_names = music_scraper.get_top_artists_names(
    last_x_weeks=2
)
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

# Grab the artists data.
artist_data_list = []

for artist_name in artists_spotify_ids:

    # Grab the artist Spotify ID.
    artist_spotify_id = artists_spotify_ids[artist_name]

    # Grab the artist data.
    artist_data = music_scraper.get_artist_by_id(
        spotify_id=artist_spotify_id
    )

    # Store the artist data
    artist_data_list.append(artist_data)

pprint(artist_data_list)

# Save the artists data.
with open('samples/responses/artists_data.jsonc', 'w+') as artists_data_file:
    json.dump(obj=artist_data_list, fp=artists_data_file, indent=2)
