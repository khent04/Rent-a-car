from app.models.user.vendor import Vendor
from app.models.user.renter import Renter
from app.models.car import Car
from ferris import BasicModel, ndb
from ferris.behaviors import searchable


class Reservation(BasicModel):
    class Meta:
        behaviors = (searchable.Searchable, )
        search_index = ('global', )


    car = ndb.KeyProperty(kind='Car', required=True, indexed=True)
    pickup_date = ndb.DateTimeProperty(required=True, indexed=False)
    pickup_place = ndb.StringProperty(required=True, indexed=False)
    dropoff_date = ndb.DateTimeProperty(required=True, indexed=False)
    dropoff_place = ndb.StringProperty(required=True, indexed=False)
    renter = ndb.KeyProperty(kind='Renter', required=True, indexed=False)
    request_code = ndb.StringProperty(required=True, indexed=False) #to be sent via email/sms?
    approved = ndb.BooleanProperty(required=True, indexed=False) #to be approved by vendor
    amount = ndb.FloatProperty(required=True, indexed=False) #compute per day price accdg to pickupdate and droppoff date
    cancelled = ndb.BooleanProperty(required=False, indexed=False)


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
