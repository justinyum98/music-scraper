"""
Script that,
given a set containing unique Spotify IDs,
returns a set containing the original set + 'relevant' artist IDs.
'Relevant' being:
- Featured in tracks
- Co-artist on albums
- Spotify's recommended related artists.

This script utilizes recursion.
[TBD]

(Pseudocode)

for top_artist_name in top_artist_names:
    
    # Search/query for artist by name:


print result
"""
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from typing import Set
from typing import List

from music_scraper.billboard import BillboardScraper

##### GET BILLBOARD TOP ARTIST NAMES #####
print("--- Getting Billboard Top 100 Artists ---")
# Record the start time.
start_time = time.time()

# Initialize the Billboard scraper.
billboard_scraper = BillboardScraper()

# Grab the top artists names from the last 2 weeks
top_artists_names = billboard_scraper.get_top_artists_names(
    last_x_weeks=2
)

# End time.
print("--- %s seconds ---" % (time.time() - start_time))

##### GET BILLBOARD TOP ARTIST SPOTIFY IDS #####
print("--- Getting Spotify Artists off Billboard Top 100 Artists ---")
# Record the start time.
start_time = time.time()

# Initialize Spotify Client with Client Credentials Flow
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# Create a set of the Billboard artists' Spotify IDs.
spotify_ids: Set[str] = set()

for top_artist_name in top_artists_names:

    # Make query URL-safe (replace space with +).
    query = top_artist_name.replace(' ', '+')

    # Search for the artist by name.
    search_result: List[dict] = sp.search(
        q=query,
        type='artist'
    )['artists']['items']

    # Check if search result is not empty.
    if search_result:
        # If so, grab the first result's Spotify ID.
        spotify_ids.add(search_result[0]['id'])

# End time.
print("--- %s seconds ---" % (time.time() - start_time))

##### GET ALL RELEVANT ARTIST SPOTIFY IDS #####
print("--- Getting relevant artists ---")
# Record the start time.
start_time = time.time()

def get_relevant_artist_ids(artist_id: str, added_artist_ids: Set[str], depth = 0, depth_limit = 1000) -> Set[str]:
    """
    Description:
    ------------
    Given an artist's Spotify ID, get all 'relevant' artists' Spotify IDs.
    'Relevant' being:
    - Co-artist on albums/singles
    - Featured in tracks
    - Spotify's recommended related artists.

    Arguments:
    ----------
    artist_id (str): Spotify ID of artist.
    added_artist_ids (Set[str]): The list of artist IDs.
    depth (int): The recursion depth.
    depth_limit (int): The recursion depth limit.

    Returns:
    --------
    Set[str]: Set containing all relevant artist Spotify IDs.
    """

    added_artist_ids_copy = added_artist_ids.copy()

    if depth > depth_limit:
        return added_artist_ids_copy

    # Grab the artist's albums
    artist_albums: List[dict] = sp.artist_albums(
        artist_id=artist_id,
        album_type='album',
        limit=50
    )['items']

    # Iterate through artist's albums.
    for artist_album in artist_albums:
        # Grab the album's artists.
        album_artists: List[dict] = artist_album['artists']

        # Iterate through the album's artists.
        for album_artist in album_artists:
            # If the id is not recorded...
            if album_artist['id'] not in added_artist_ids_copy:
                # Add the id.
                added_artist_ids_copy.add(album_artist['id'])
                
                # If the depth doesn't exceed 10...
                if depth + 1 < depth_limit:
                    # Grab the artist's relevant artists, get the union, update the added artist ids.
                    added_artist_ids_copy = added_artist_ids_copy.union(
                        get_relevant_artist_ids(
                            artist_id=album_artist['id'],
                            added_artist_ids=added_artist_ids_copy,
                            depth=depth+1,
                            depth_limit=depth_limit
                        )
                    )

        # Grab the album's tracks.
        album_tracks: List[dict] = sp.album_tracks(
            album_id=artist_album['id']
        )['items']

        # Iterate through album's tracks.
        for album_track in album_tracks:
            # Grab the track's artists.
            track_artists: List[dict] = album_track['artists']

            # Iterate through the track's artists.
            for track_artist in track_artists:
                # If the id is not recorded...
                if track_artist['id'] not in added_artist_ids_copy:
                    # Add the id.
                    added_artist_ids_copy.add(track_artist['id'])

                    # If the depth doesn't exceed 10...
                    if depth + 1 < depth_limit:
                        # Grab the artist's relevant artists, get the union, update the added artist ids.
                        added_artist_ids_copy = added_artist_ids_copy.union(
                            get_relevant_artist_ids(
                                artist_id=track_artist['id'],
                                added_artist_ids=added_artist_ids_copy,
                                depth=depth+1,
                                depth_limit=depth_limit
                            )
                        )

    # Grab the artist's singles.
    artist_singles: List[dict] = sp.artist_albums(
        artist_id=artist_id,
        album_type='single',
        limit=50
    )['items']

    # Iterate through artist's singles.
    for artist_single in artist_singles:
        # Grab the single's artists.
        single_artists: List[dict] = artist_single['artists']

        # Iterate through the single's artists.
        for single_artist in single_artists:
            # If the id is not recorded...
            if single_artist['id'] not in added_artist_ids_copy:
                # Add the id
                added_artist_ids_copy.add(single_artist['id'])

                # If the depth doesn't exceed 10...
                if depth + 1 < depth_limit:
                    # Grab the artist's relevant artists, get the union, update the added artist ids.
                    added_artist_ids_copy = added_artist_ids_copy.union(
                        get_relevant_artist_ids(
                            artist_id=single_artist['id'],
                            added_artist_ids=added_artist_ids_copy,
                            depth=depth+1,
                            depth_limit=depth_limit
                        )
                    )

        # Grab the single's tracks.
        single_tracks: List[dict] = sp.album_tracks(
            album_id=artist_single['id']
        )['items']

        # Iterate through the single's tracks.
        for single_track in single_tracks:
            # Grab the track's artists.
            track_artists: List[dict] = single_track['artists']

            # Iterate through the track's artists.
            for track_artist in track_artists:
                # If the id is not recorded...
                if track_artist['id'] not in added_artist_ids_copy:
                    # Add the id.
                    added_artist_ids_copy.add(track_artist['id'])

                    # If the depth doesn't exceed limit...
                    if depth + 1 < depth_limit:
                        # Grab the artist's relevant artists, get the union, update the added artist ids.
                        added_artist_ids_copy = added_artist_ids_copy.union(
                            get_relevant_artist_ids(
                                artist_id=track_artist['id'],
                                added_artist_ids=added_artist_ids_copy,
                                depth=depth+1,
                                depth_limit=depth_limit
                            )
                        )

    # Grab an artist's related artists.
    related_artists: List[dict] = sp.artist_related_artists(
        artist_id=artist_id
    )['artists']
    
    # Iterate through the artist's related artists.
    for related_artist in related_artists:
        # If the id is not recorded...
        if related_artist['id'] not in added_artist_ids_copy:
            # Add the id.
            added_artist_ids_copy.add(related_artist['id'])
            print('Adding new artist: ' + related_artist['name'])
            # Grab the artist's relevant artists, get the union, update the added artist ids.
            added_artist_ids_copy = added_artist_ids_copy.union(
                get_relevant_artist_ids(
                    artist_id=related_artist['id'],
                    added_artist_ids=added_artist_ids_copy
                )
            )

    # Return the result.
    return added_artist_ids_copy
##### END OF ALGORITHM #####

all_spotify_ids = spotify_ids.copy()

for artist_id in spotify_ids:

    added_spotify_ids = all_spotify_ids.copy()

    # Grab relevant artist ids.
    relevant_artist_ids = get_relevant_artist_ids(
        artist_id=artist_id,
        added_artist_ids=added_spotify_ids,
        # ! Set the depth here.
        depth_limit=1
    )

    # Get the union of the two sets.
    all_spotify_ids = all_spotify_ids.union(relevant_artist_ids)

# End time.
print("--- %s seconds ---" % (time.time() - start_time))

##### NOW, TO GRAB ARTISTS #####
"""
Now, to store the data in the database:
(Pseudocode)

# Get artists.
artists = {}

for spotify_id in all_spotify_ids:
    get artist with 'spotify_id'
    append artist to 'artists' (key=spotify_id, value=artist)
"""
print('--- Getting all artists ---')
# Record the start time.
start_time = time.time()

# Initialize list of artists.
artists = {}

# Iterate through artist Spotify IDs.
for spotify_id in all_spotify_ids:

    # Grab artist.
    artist = sp.artist(artist_id=spotify_id)

    # Grab data from artist.
    mini_dict = {}
    mini_dict['name'] = artist['name']
    mini_dict['spotify_id'] = artist['id']
    if artist['images']:
        mini_dict['profile_picture_url'] = artist['images'][0]['url']
    mini_dict['genres'] = artist['genres']

    # Append data to artists.
    artists[spotify_id] = mini_dict

# End time.
print("--- %s seconds ---" % (time.time() - start_time))

# Save the Spotify artists.
with open('samples/responses/spotify_artists.jsonc', 'w+') as spotify_artists_file:
    json.dump(obj=artists, fp=spotify_artists_file, indent=2)
