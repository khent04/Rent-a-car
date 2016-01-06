from ferris import BasicModel, ndb, model_form
from google.appengine.api import images


class MediaUploader(BasicModel):
    file = ndb.BlobKeyProperty()
    file_cloud_storage = ndb.StringProperty()
    tags = ndb.StringProperty()
    image_serving_url = ndb.StringProperty(indexed=False)


    def before_put(self):
        if self.file:
            self.image_serving_url = images.get_serving_url(self.file, secure_url=False)
        else:
            self.image_serving_url = None

    @classmethod
    def create(cls, **params):
        item = cls(**params)
        item.put()
        return item

    def update(self, **params):
        self.populate(**params)
        self.put()

    def delete(self):
        ndb.delete_multi(ndb.Query(ancestor=self.key).iter(keys_only=True))


class MediaUploaderForm(model_form(MediaUploader, exclude=('image_serving_url',))):
    pass
