from ferris import BasicModel, ndb, model_form
from google.appengine.api import images


class Certificate(BasicModel):
    file = ndb.BlobKeyProperty()
    tags = ndb.StringProperty()
    image_serving_url = ndb.StringProperty(indexed=False)
    file_name = ndb.StringProperty(indexed=False)


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


class CertificateForm(model_form(Certificate, exclude=('image_serving_url',))):
    pass
