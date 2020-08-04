import mongoengine


class Album(mongoengine.Document):
    title = mongoengine.StringField(
        required=True
    )
    spotifyId = mongoengine.StringField(
        default=None
    )
    description = mongoengine.StringField(
        default=None
    )
    coverArtUrl = mongoengine.URLField(
        default=None
    )
    albumType = mongoengine.StringField()
    artists = mongoengine.ListField(
        mongoengine.ReferenceField('Artist')
    )
    tracks = mongoengine.ListField(
        mongoengine.ReferenceField('Song')
    )
    releaseDate = mongoengine.DateField()
    posts = mongoengine.ListField(
        mongoengine.ReferenceField('Post')
    )
    likes = mongoengine.IntField(
        default=0
    )
    likers = mongoengine.ListField(
        mongoengine.ReferenceField('User')
    )
