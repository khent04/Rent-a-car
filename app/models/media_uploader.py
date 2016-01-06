from ferris import BasicModel, ndb


class MediaUploader(BasicModel):
    file = ndb.BlobKeyProperty()
    file_cloud_storage = ndb.StringProperty()
    tags = ndb.StringProperty()

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
