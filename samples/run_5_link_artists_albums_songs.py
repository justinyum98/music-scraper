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
