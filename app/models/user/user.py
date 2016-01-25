from app.behaviors.unique import Unique, format_key_name
from ferris import BasicModel, ndb, messages
from ferris.behaviors import searchable
from protopigeon.converters import Converter, KeyConverter, converters as default_converters
from google.appengine.ext.ndb import polymodel


class ReferenceToValueConverter(Converter):
    @staticmethod
    def to_message(Mode, property, field, value):
        return str(value.get())

    @staticmethod
    def to_field(Model, property, count):
        return messages.StringField(count, repeated=property._repeated)

key_converter = {'KeyProperty': ReferenceToValueConverter}


class User(BasicModel, polymodel.PolyModel):
    class Meta:
        behaviors = (Unique, searchable.Searchable, )
        uniqueness_identifier = 'email'
        search_index = ('global',)

    email = ndb.StringProperty(required=True, indexed=True)
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)
    contact_number = ndb.StringProperty(indexed=True)
    postal_code = ndb.StringProperty(indexed=False)

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
