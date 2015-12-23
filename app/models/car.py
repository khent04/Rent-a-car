from app.behaviors.unique import format_key_name
from ferris import BasicModel, ndb
from ferris.behaviors import searchable


class Car(BasicModel):
    class Meta:
        behaviors = (searchable.Searchable, )
        search_index = ('global',)

    model = ndb.StringProperty(required=True, indexed=False)
    transmission = ndb.StringProperty(required=False, indexed=False)
    # manual/auto
    price = ndb.FloatProperty(required=True, indexed=False)
    # in dollar and per day
    category = ndb.StringProperty(required=False, indexed=False)
    availability = ndb.BooleanProperty(required=False, indexed=False)
    location = ndb.StringProperty(required=False, indexed=False)
    # ask the vendor if the car is the same with his address,
    # if not ask for manual input of address
    seats = ndb.IntegerProperty(required=False, indexed=True)
    trunk_capacity = ndb.IntegerProperty(required=False, indexed=False)
    air_conditioned = ndb.BooleanProperty(required=False, indexed=False)
    mileage = ndb.StringProperty(required=False, indexed=False)
    # ask user if unlimited, if not ask for mileage
    age = ndb.IntegerProperty(required=False, indexed=True)
    # image_serving_url = ndb.StringProperty(indexed=False)

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
