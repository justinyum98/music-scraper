import mongoengine


class Song(mongoengine.Document):
    title = mongoengine.StringField(
        required=True
    )
    spotifyId = mongoengine.StringField(
        default=None
    )
    description = mongoengine.StringField(
        default=None
    )
    explicit = mongoengine.BooleanField(
        required=True
    )
    discNumber = mongoengine.IntField(
        default=1
    )
    trackNumber = mongoengine.IntField(
        required=True
    )
    duration = mongoengine.IntField(
        required=True
    )
    artists = mongoengine.ListField(
        mongoengine.ReferenceField('Artist')
    )
    album = mongoengine.ReferenceField('Album')
    posts = mongoengine.ListField(
        mongoengine.ReferenceField('Post')
    )
    likes = mongoengine.IntField(
        default=0
    )
    likers = mongoengine.ListField(
        mongoengine.ReferenceField('User')
    )
