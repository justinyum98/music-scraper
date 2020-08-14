"""
Script for storing artists, albums, and tracks in database.

(Pseudocode)

# Get artist_data from json file.
artists_data: dict

for artist_id in artists_data:
    # Get the artist
    artist = artists_data[artist_id]
    
    # Create the artist
    artist_doc_id = 

"""
import os
import json
import time
import mongoengine

from typing import List

from music_scraper.artist import Artist
from music_scraper.album import Album
from music_scraper.track import Track

print('--- STORE IN DB SCRIPT ---')
start_time = time.time()

# Connect to database.
mongodb_uri = os.environ['MONGODB_URI']
mongoengine.connect('development', host=mongodb_uri)

# Load artist data.
with open(file=r'samples/responses/spotify_artists_data.jsonc', mode='r') as spotify_artists_data_file:
    artists_data: dict = json.load(fp=spotify_artists_data_file)

print('Number of artists:', len(artists_data.keys()))

##### HELPER FUNCTIONS #####
def artist_exists(spotify_id: str) -> bool:
    matches = Artist.objects(spotifyId=spotify_id).count()
    if matches == 0:
        return False
    return True

def album_exists(spotify_id: str) -> bool:
    matches = Album.objects(spotifyId=spotify_id).count()
    if matches == 0:
        return False
    return True

def track_exists(spotify_id: str) -> bool:
    matches = Track.objects(spotifyId=spotify_id).count()
    if matches == 0:
        return False
    return True

##### END of HELPER FUNCTIONS #####

print('Running script...')
# Iterate through artists.
for artist_id in artists_data:
    # Get the artist
    artist: dict = artists_data[artist_id]

    # Check if artist doesn't exist in db.
    if not artist_exists(artist['spotify_id']):
        # Create & save the artist
        if 'profile_picture_url' not in artist:
            profile_picture_url = None
        else:
            profile_picture_url = artist['profile_picture_url']

        artist_doc = Artist(
            name=artist['name'],
            spotifyId=artist['spotify_id'],
            profilePictureUrl=profile_picture_url,
            genres=artist['genres']
        )
        artist_doc.save()

    # Iterate through artist's albums
    for album in artist['albums']:
        # Check if album doesn't exist in db.
        if not album_exists(album['spotify_id']):
            # Create & save the album
            if 'cover_art_url' not in album:
                cover_art_url = None
            else:
                cover_art_url = album['cover_art_url']

            album_doc = Album(
                title=album['title'],
                spotifyId=album['spotify_id'],
                coverArtUrl=cover_art_url,
                albumType=album['album_type'],
                releaseDate=album['release_date']
            )
            album_doc.save()

        # Iterate through album's tracks
        for track in album['tracks']:
            # Check if song doesn't exist in db.
            if not track_exists(track['spotify_id']):
                # Create & save the song
                track_doc = Track(
                    title=track['title'],
                    spotifyId=track['spotify_id'],
                    explicit=track['explicit'],
                    discNumber=track['disc_number'],
                    trackNumber=track['track_number'],
                    duration=track['duration'],
                )
                track_doc.save()

print("--- Done: Took %s seconds ---" % (time.time() - start_time))
