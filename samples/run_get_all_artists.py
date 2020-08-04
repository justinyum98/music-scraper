"""
Script that grabs every relevant artist in the data set.
Given a list of artists...
(Pseudocode)

result = {}

for artist in artists:
    get the artist data
    add to result dict (key = artist name, value = artist data)

    get the artist's albums (and singles)
    for album in albums:
        get album's artists
        for album_artist in album_artists:
            if album_artist name not in result.keys():
                get the album_artist data
                add to result dict
        
        get the album's tracks
        for track in tracks:
            get track's artists
            for track_artist in track_artists:
                if track_artist name not in result.keys():
                    get the track_artist data
                    add to result dict

print result
"""
