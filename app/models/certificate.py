from ferris import BasicModel, ndb
from google.appengine.api import images


class Certificate(BasicModel):
    name = ndb.StringProperty(required=True, indexed=True)
    image = ndb.BlobKeyProperty(indexed=False)
    image_serving_url = ndb.StringProperty(indexed=False)
    approved = ndb.BooleanProperty(default=False, indexed=False)
    uploader = ndb.KeyProperty(kind='User', indexed=False)

    def before_put(self):
        if self.image:
            self.image_serving_url = images.get_serving_url(self.image,
                                                            secure_url=False)
        else:
            self.image_serving_url = None

    @classmethod
    def create(cls, **params):
        item = cls(**params)
        item.put()
        return item
