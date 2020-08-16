import mongoengine


class Album(mongoengine.Document):
    title = mongoengine.StringField(
        required=True
    )
    spotifyId = mongoengine.StringField(
        default=None,
        unique=True
    )
    description = mongoengine.StringField(
        default=None
    )
    coverArtUrl = mongoengine.URLField(
        default=None
    )
    albumType = mongoengine.StringField(
        required=True
    )
    artists = mongoengine.ListField(
        mongoengine.ReferenceField('Artist')
    )
    tracks = mongoengine.ListField(
        mongoengine.ReferenceField('Track')
    )
    releaseDate = mongoengine.StringField(
        default=None
    )
    posts = mongoengine.ListField(
        mongoengine.ReferenceField('Post')
    )
    likes = mongoengine.IntField(
        default=0
    )
    likers = mongoengine.ListField(
        mongoengine.ReferenceField('User')
    )
    meta = {
        'collection': 'albums'
    }
