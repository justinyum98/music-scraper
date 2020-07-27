class SpotifyParser():
    def parse_artist_data(self, response_data: dict) -> dict:
        """Given a Spotify Artist object, grab the data you need.

        https://developer.spotify.com/documentation/web-api/reference/object-model/#artist-object-full
        """
        artist_data = {}

        # (1) Grab the artist's name.
        artist_data['name'] = response_data['name']

        # (2) Grab the artist's profile picture urls.
        profile_picture_urls = []
        for image in response_data['images']:
            profile_picture_urls.append(image['url'])
        artist_data['images'] = profile_picture_urls

        # (3) Grab the artist's genre(s).
        artist_data['genres'] = response_data['genres']

        return artist_data
