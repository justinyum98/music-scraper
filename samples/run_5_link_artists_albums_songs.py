"""
Script that links:
1) Artists to their Albums.
2) Albums to their Artists and Songs.
3) Songs to their Artists and Album.

(Pseudocode)
Get 'spotify_artists_data.jsonc' data

for artist_id in spotify_artists_data:
    # Get the artist
    artist: dict = spotify_artists_data[artist_id]

    # Get the artist's albums.
    artist_albums: List[dict] = artist['albums']

    # Iterate through artist's albums.
    for album in artist_albums:
        # Get the album document by spotify id
        # ! If album not found, throw error
        album_doc = Album.objects(spotifyId=artist_album['spotify_id'])[0]

        # Get the album's artists.
        album_artists = album['artists']

        # Iterate through the album's artists
        for album_artist in album_artists:
            # Get the artist document by spotify id
            # ! If artist not found, throw Error.
            album_artist_doc = Artist.objects(spotifyId=album_artist['id'])[0]

            # Link album's artists with album, and vice versa.
            # Check if album_artist --> album
            if album_artist_doc.id not in album_doc.artists:
                album_doc.artists.append(album_artist_doc.id)
                album_doc.save()

            # Check if album --> album_artist:
            if album_doc.id not in album_artist_doc.albums:
                album_artist_doc.albums.append(album_doc.id)
                album_artist_doc.save()

        # Iterate through the album's tracks
        for track in album['tracks']:
            # Get the track document by spotify id
            # ! If track not found, throw Error.
            track_doc = Track.objects(spotifyId=track['spotify_id'])[0]

            # Link track with it's album, and vice versa
            # Check if track --> album
            if track_doc.id not in album_doc.tracks:
                album_doc.tracks.append(track_doc.id)
                album_doc.save()

            # Check if album --> track:
            if album_doc.id != track_doc.album:
                track_doc.album = album_doc.id
                track_doc.save()

            # Iterate through track's artists.
            for track_artist in track['artists']:
                # Get the track's artist by spotify id
                # ! If artist not found, throw Error.
                track_artist_doc = Artist.objects(spotifyId=track_artist['id'])

                # Link track with it's artist(s), and vice versa
                # Check if track_artist --> track
                if track_artist_doc.id not in track_doc.artists:
                    track_doc.artists.append(track_artist_doc.id)
                    track_doc.save()
"""
import os
import json
import time
import mongoengine
from bson.objectid import ObjectId

from typing import List

from music_scraper.artist import Artist
from music_scraper.album import Album
from music_scraper.track import Track

print('--- RUNNING LINK DB ARTIST ALBUM SONG SCRIPT ---')
start_time = time.time()

print('Connecting to database...')
mongodb_uri = os.environ['MONGODB_URI']
mongoengine.connect('development', host=mongodb_uri)

print('Loading artist data set...')
with open(file=r'samples/responses/spotify_artists_data.jsonc', mode='r') as spotify_artists_data_file:
    artists_data: dict = json.load(fp=spotify_artists_data_file)

def check_if_album_contains_artist(artist_id, album_doc: Album) -> bool:
    for album_artist in album_doc.artists:
        if isinstance(album_artist, Artist):
            return artist_id == album_artist.id
        elif isinstance(album_artist, ObjectId):
            return artist_id == album_artist
    
    return False

def check_if_artist_contains_album(album_id, artist_doc: Artist) -> bool:
    for artist_album in artist_doc.albums:
        if isinstance(artist_album, Album):
            return album_id == artist_album.id
        elif isinstance(artist_album, ObjectId):
            return album_id == artist_album

    return False

def check_if_album_contains_track(track_id, album_doc: Album) -> bool:
    for track in album_doc.tracks:
        if isinstance(track, Track):
            return track_id == track.id
        elif isinstance(track, ObjectId):
            return track_id == track

    return False

def check_if_track_contains_album(album_id, track_doc: Track) -> bool:
    if isinstance(track_doc.album, Album):
        return album_id == track_doc.album.id
    elif isinstance(track_doc.album, ObjectId):
        return album_id == track_doc.album
    elif track_doc.album is None:
        return False
    else:
        raise TypeError("Track document's type is neither Album or ObjectId")

def check_if_track_contains_artist(artist_id, track_doc: Track) -> bool:
    for artist in track_doc.artists:
        if isinstance(artist, Artist):
            return artist_id == artist.id
        if isinstance(artist, ObjectId):
            return artist_id == artist

    return False
        

print('Starting script.')
for artist_id in artists_data:
    # Get the artist
    artist: dict = artists_data[artist_id]

    # Get the artist's albums.
    artist_albums: List[dict] = artist['albums']

    # Iterate through artist's albums.
    for album in artist_albums:
        # Get the album document by spotify id
        # ! If album not found, throw Error.
        album_doc: Album = Album.objects(
            spotifyId=album['spotify_id']).first()

        # Get the album's artists.
        album_artists: List[dict] = album['artists']

        # Iterate through the album's artists
        for album_artist in album_artists:
            # Get the artist document by spotify id
            # ! If artist not found, throw Error.
            album_artist_doc: Artist = Artist.objects(spotifyId=album_artist['id']).first()

            if album_artist_doc != None:
                # Link album's artists with album, and vice versa.
                # Check if album_artist --> album
                if not check_if_album_contains_artist(artist_id=album_artist_doc.id, album_doc=album_doc):
                    album_doc.artists.append(album_artist_doc.id)
                    album_doc.save()

                # Check if album --> album_artist:
                if not check_if_artist_contains_album(album_id=album_doc.id, artist_doc=album_artist_doc):
                    album_artist_doc.albums.append(album_doc.id)
                    album_artist_doc.save()

        # Iterate through the album's tracks
        for track in album['tracks']:
            # Get the track document by spotify id
            # ! If track not found, throw Error.
            track_doc: Track = Track.objects(spotifyId=track['spotify_id']).first()

            if track_doc != None:
                # Link track with it's album, and vice versa
                # Check if track --> album
                if not check_if_album_contains_track(track_id=track_doc.id, album_doc=album_doc):
                    album_doc.tracks.append(track_doc.id)
                    album_doc.save()

                # Check if album --> track:
                if not check_if_track_contains_album(album_id=album_doc.id, track_doc=track_doc):
                    track_doc.album = album_doc.id
                    track_doc.save()

            # Iterate through track's artists.
            for track_artist in track['artists']:
                # Get the track's artist by spotify id
                # ! If artist not found, throw Error.
                track_artist_doc: Artist = Artist.objects(
                    spotifyId=track_artist['id']).first()

                if track_artist_doc != None:
                    # Link track with it's artist(s), and vice versa
                    # Check if track_artist --> track
                    if not check_if_track_contains_artist(artist_id=track_artist_doc.id, track_doc=track_doc):
                        track_doc.artists.append(track_artist_doc.id)
                        track_doc.save()

print("--- DONE: %s seconds ---" % (time.time() - start_time))
