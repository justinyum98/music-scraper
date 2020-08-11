import json
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from typing import List

# Initialize Spotify Client with Client Credentials Flow
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# Load Spotify artists.
with open(file=r'samples/responses/spotify_artists.jsonc', mode='r') as spotify_artists_file:
    spotify_artists: dict = json.load(fp=spotify_artists_file)

# Get the list of Spotify IDs.
spotify_artist_ids: List[str] = spotify_artists.keys()

print('--- GETTING ARTIST DATA ---')
start_time = time.time()
##### Get the artists' albums and their tracks #####
for artist_id in spotify_artist_ids:
    
    # Get the artist's albums.
    artist_albums: List[dict] = sp.artist_albums(
        artist_id=artist_id,
        album_type='album',
        limit=50
    )['items']

    # Get the artist's singles.
    artist_singles: List[dict] = sp.artist_albums(
        artist_id=artist_id,
        album_type='single',
        limit=50
    )['items']

    # Combine the two.
    albums: List[dict] = artist_albums + artist_singles

    # Initialize the albums result.
    albums_data = []

    # Iterate through albums.
    for album in albums:

        album_data = {}
        album_data['title'] = album['name']
        album_data['spotify_id'] = album['id']
        if album['images']:
            album_data['cover_art_url'] = album['images'][0]['url']
        album_data['album_type'] = album['album_type']
        album_data['artists'] = album['artists']
        album_data['release_date'] = album['release_date']

        # Get the album's tracks.
        album_tracks: List[dict] = sp.album_tracks(
            album_id=album['id']
        )['items']

        # Initialize the tracks result.
        tracks_data = []

        # Iterate through the tracks.
        for album_track in album_tracks:
            track_data = {}
            track_data['title'] = album_track['name']
            track_data['spotify_id'] = album_track['id']
            track_data['explicit'] = album_track['explicit']
            track_data['disc_number'] = album_track['disc_number']
            track_data['track_number'] = album_track['track_number']
            track_data['duration'] = album_track['duration_ms']
            track_data['artists'] = album_track['artists']
            track_data['album'] = album['id']

            tracks_data.append(track_data)

        album_data['tracks'] = tracks_data

        albums_data.append(album_data)
    
    spotify_artists[artist_id]['albums'] = albums_data

print("--- Done: Took %s seconds ---" % (time.time() - start_time))

# Save the Spotify artists data.
with open('samples/responses/spotify_artists_data.jsonc', 'w+') as spotify_artists_data_file:
    json.dump(obj=spotify_artists, fp=spotify_artists_data_file, indent=2)
