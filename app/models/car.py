from app.behaviors.unique import format_key_name
from ferris import BasicModel, ndb, messages
from ferris.behaviors import searchable
from protopigeon.converters import Converter, KeyConverter, DateConverter, converters as default_converters

class ReferenceToValueConverter(Converter):
    @staticmethod
    def to_message(Mode, property, field, value):
        return str(value.get())

    @staticmethod
    def to_field(Model, property, count):
        return messages.StringField(count, repeated=property._repeated)

key_converter = {'KeyProperty': ReferenceToValueConverter}


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
        field_dict['company'] = messages.StringField(count + 1, required=True)
        field_dict['credibility'] = messages.IntegerField(count + 2, required=True)
        return type('user_full_message', (messages.Message,), field_dict)

    @staticmethod
    def transform_message(entity, message):
        return message(
            key=KeyConverter.to_message(None, None, None, entity.key),
            car_model=entity.car_model,
            location=entity.location,
            seats=entity.seats,
            trunk_capacity=entity.trunk_capacity,
            air_conditioned=entity.air_conditioned,
            mileage=entity.mileage,
            age=entity.age,
            transmission=entity.transmission,
            category=entity.category,
            availability=entity.availability,
            price=entity.price,
            vendor=entity.vendor.get().email,
            company=entity.vendor.get().company,
            credibility=entity.vendor.get().credibility
        )


