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
import json
from pprint import pprint
import requests

from typing import Set
from typing import List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from music_scraper.billboard import BillboardScraper

# Initialize the Billboard scraper.
billboard_scraper = BillboardScraper()

# Grab the top artists names from the last 2 weeks
top_artists_names = billboard_scraper.get_top_artists_names(
    last_x_weeks=2
)
pprint(top_artists_names)

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

pprint(spotify_ids)

