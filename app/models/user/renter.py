from google.appengine.ext import ndb
from app.models.user.user import User
from ferris import messages
from protopigeon.converters import Converter, KeyConverter, converters as default_converters



class ReferenceToValueConverter(Converter):
    @staticmethod
    def to_message(Mode, property, field, value):
        return str(value.get())

    @staticmethod
    def to_field(Model, property, count):
        return messages.StringField(count, repeated=property._repeated)

key_converter = {'KeyProperty': ReferenceToValueConverter}


class Renter(User):

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
    def full_message(cls):
        field_dict, count = cls.message_props(converters=key_converter)
        field_dict['user_type'] = messages.StringField(count + 1, required=True)
        return type('user_full_message', (messages.Message,), field_dict)

    @staticmethod
    def transform_message(entity, message):
        return message(
            key=KeyConverter.to_message(None, None, None, entity.key),
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            contact_number=entity.contact_number,
            postal_code=entity.postal_code,
            user_type=entity._class_name(),
        )
