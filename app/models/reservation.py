from app.behaviors.unique import format_key_name
from ferris import BasicModel, ndb, messages
from ferris.behaviors import searchable
from protopigeon.converters import Converter, KeyConverter, DateConverter, converters as default_converters
import datetime

class ReferenceToValueConverter(Converter):
    @staticmethod
    def to_message(Mode, property, field, value):
        return str(value.get())

    @staticmethod
    def to_field(Model, property, count):
        return messages.StringField(count, repeated=property._repeated)

key_converter = {'KeyProperty': ReferenceToValueConverter}

class Reservation(BasicModel):
    class Meta:
        behaviors = (searchable.Searchable, )
        search_index = ('global', )

    car = ndb.KeyProperty(kind='Car', required=True, indexed=True)
    pickup_date = ndb.DateProperty(required=True, indexed=False)
    pickup_time = ndb.StringProperty(required=True, indexed=False)
    pickup_place = ndb.StringProperty(required=True, indexed=False)
    dropoff_date = ndb.DateProperty(required=True, indexed=False)
    dropoff_time = ndb.StringProperty(required=True, indexed=False)
    drop_location = ndb.StringProperty(required=True, indexed=False)
    renter = ndb.KeyProperty(kind='User', required=True, indexed=True)
    request_code = ndb.StringProperty(required=True, indexed=False)
    # to be sent via email/sms?
    approved = ndb.BooleanProperty(default=False, indexed=True)
    rejected = ndb.BooleanProperty(default=False, indexed=True)
    # to be approved by vendor
    amount = ndb.FloatProperty(required=True, indexed=False)
    # compute per day price accdg to pickupdate and droppoff date
    cancelled = ndb.BooleanProperty(default=False, indexed=True)
    expired = ndb.BooleanProperty(default=False, indexed=True)
    rating = ndb.IntegerProperty(default=1, indexed=True)

    @classmethod
    def create(cls, **params):
        item = cls(**params)
        item.put()
        return item

    def update(self, **params):
        self.populate(**params)
        self.put()

    @classmethod
    def list(cls, approved):
        return cls.query(cls.approved == approved, cls.rejected == False, cls.expired == False, cls.cancelled == False).fetch()

    @classmethod
    def rentals(cls, renter):
        return cls.query(cls.renter == renter)

    @classmethod
    def compute_credibility(cls, vendor):
        data = cls.query(cls.approved == True, cls.rejected == False)
        tmp_rates = []
        if data:
            data = data.fetch()
            tmp_rates = [x.rating * 20 for x in data if x.car.get().vendor == vendor]

        return sum(tmp_rates)/len(tmp_rates)

    @classmethod
    def message_props(cls, only=None, exclude=None, converters=None):
        props = cls._properties
        sorted_props = sorted(props.iteritems(), key=lambda prop: prop[1]._creation_counter)
        field_names = [x[0] for x in sorted_props if x[0]]
        if exclude:
            field_names = [x for x in field_names if x not in exclude]
        if only:
            field_names = [x for x in field_names if x in only]
        converters = dict(default_converters.items() + converters.items()) if converters else default_converters
        key_holder = type('', (), {})()
        key_holder.name = 'key',
        key_holder._repeated = False
        field_dict = {
            'key': converters['Key'].to_field(cls, key_holder, 1)
        }
        last_count = 0
        for count, name in enumerate(field_names, start=2):
            last_count = count
            prop = props[name]
            converter = converters.get(prop.__class__.__name__, None)
            if converter:
                field_dict[name] = converter.to_field(cls, prop, count)
        return field_dict, last_count

    @classmethod
    def message(cls):
        field_dict, count = cls.message_props(converters=key_converter)
        return type('car', (messages.Message,), field_dict)

    @staticmethod
    def car_message(entity, message):
        ret = messages.to_message(entity, message)
        return ret

    @classmethod
    def full_message(cls):
        field_dict, count = cls.message_props(converters=key_converter)
        field_dict['car'] = messages.StringField(count + 1, required=True)
        field_dict['renter'] = messages.StringField(count + 2, required=True)
        field_dict['vendor'] = messages.StringField(count + 3, required=True)
        field_dict['company'] = messages.StringField(count + 4, required=True)
        field_dict['company'] = messages.StringField(count + 4, required=True)
        field_dict['rating'] = messages.IntegerField(count + 5, required=True)
        field_dict['transaction_done'] = messages.BooleanField(count + 6, required=True)

        return type('user_full_message', (messages.Message,), field_dict)

    @staticmethod
    def transform_message(entity, message):
        return message(
            key=KeyConverter.to_message(None, None, None, entity.key),
            car=entity.car.get().car_model,
            pickup_date=DateConverter.to_message(None, None, None, entity.pickup_date),
            pickup_time=entity.pickup_time,
            pickup_place=entity.pickup_place,
            dropoff_date=DateConverter.to_message(None, None, None, entity.dropoff_date),
            dropoff_time=entity.dropoff_time,
            drop_location=entity.drop_location,
            request_code=entity.request_code,
            approved=entity.approved,
            rejected=entity.rejected,
            amount=entity.amount,
            cancelled=entity.cancelled,
            renter=entity.renter.get().email,
            vendor=entity.car.get().vendor.get().email,
            company=entity.car.get().vendor.get().company,
            rating=entity.rating,
            expired=entity.expired,
            transaction_done=entity.pickup_date < datetime.date.today() # rating can only be shown for successful transaction, and that trnasaction is done
        )

