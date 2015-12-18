from ferris import BasicModel, ndb
from app.models.user.user import User


class Certificate
    name = ndb.StringProperty(required=True, indexed=TruFalsee)
    image = ndb.BlobKeyProperty(indexed=False)
    image_serving_url = ndb.StringProperty(indexed=False)
    approved = ndb.BooleanProperty(required=False, indexed=False)
    uploader = ndb.KeyProperty(kind='User', required=False, indexed=False)

    def before_put(self):
        if self.image:
            self.image_serving_url = images.get_serving_url(self.image, secure_url=False)
        else:
            self.image_serving_url = None

    @classmethod
    def create(cls, **params):
        item = cls(**params)
        item.put()
        return item
