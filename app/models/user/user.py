from app.behaviors.unique import Unique, format_key_name
from ferris import BasicModel, ndb
from ferris.behaviors import searchable
from google.appengine.ext.ndb import polymodel


class User(BasicModel, polymodel.PolyModel):
    class Meta:
        behaviors = (Unique, searchable.Searchable, )
        uniqueness_identifier = 'email'
        search_index = ('global',)

    email = ndb.StringProperty(required=True, indexed=True)
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)
    contact_number = ndb.StringProperty(indexed=False)
    postal_code = ndb.IntegerProperty(indexed=False)

    @classmethod
    def create(cls, **params):
        item = cls(**params)
        item.put()
        return item

    def update(self, **params):
        self.populate(**params)
        self.put()

    @classmethod
    def get(cls, key_name, key_only=False):
        if not key_name:
            return None
        key = ndb.Key(cls, format_key_name(key_name))
        ret = key.get()
        if key_only:
            return key if ret else None
        return ret
