import mongoengine


class Artist(mongoengine.Document):
    name = mongoengine.StringField(
        required=True
    )
    user = mongoengine.ReferenceField('User')
    spotifyId = mongoengine.StringField(
        default=None,
        unique=True
    )
    biography = mongoengine.StringField(
        default=None
    )
    profilePictureUrl = mongoengine.URLField(
        default=None
    )
    genres = mongoengine.ListField(
        mongoengine.StringField()
    )
    albums = mongoengine.ListField(
        mongoengine.ReferenceField('Album')
    )
    posts = mongoengine.ListField(
        mongoengine.ReferenceField('Post')
    )
    likes = mongoengine.IntField(
        default=0
    )
    likers = mongoengine.ReferenceField('User')
    meta = {
        'collection': 'artists'
    }
