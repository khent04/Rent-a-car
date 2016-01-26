from app.behaviors.unique import format_key_name
from ferris import BasicModel, ndb
from ferris.behaviors import searchable


class Car(BasicModel):
    class Meta:
        behaviors = (searchable.Searchable, )
        search_index = ('global',)

    car_model = ndb.StringProperty(required=True, indexed=False)
    transmission = ndb.StringProperty(indexed=False)
    # manual/auto
    price = ndb.FloatProperty(required=True, indexed=False)
    # in dollar and per day
    category = ndb.StringProperty(indexed=False)
    availability = ndb.BooleanProperty(default=False, indexed=True)
    location = ndb.StringProperty(indexed=True)
    # ask the vendor if the car is the same with his address,
    # if not ask for manual input of address
    seats = ndb.IntegerProperty(indexed=True)
    trunk_capacity = ndb.FloatProperty(indexed=False)
    air_conditioned = ndb.BooleanProperty(default=False, indexed=False)
    mileage = ndb.StringProperty(indexed=False)
    # ask user if unlimited, if not ask for mileage
    age = ndb.IntegerProperty(indexed=True)
    # image_serving_url = ndb.StringProperty(indexed=False)
    vendor = ndb.KeyProperty(kind="User", indexed=True)

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

    @classmethod
    def list_by_vendor(cls, vendor):
        return cls.query(cls.vendor == vendor)

    @classmethod
    def basic_search(cls, params):
        query = cls.query(cls.availability == True).fetch()
        query = [x for x in query if params['pickup_place'].lower() in x.location or x.location in [y for y in params['pickup_place'].lower().split(" ")]]
        return query
