from ferris import Model, ndb
from ferris.core.ndb import Behavior


class Unique(Behavior):
    """
    Raises `UniqueError` if the property value already exists

    Meta properties:
    * uniqueness_identifier - property name that you want to be unique
    * reference_list - list containing strings of `model.property` pairs
                where the entity is being referenced in a KeyProperty

    ex:
        class RelModel(Model):

            name = ndb.StringProperty(required=True)
            single = ndb.KeyProperty()
            multiple = ndb.KeyProperty(repeated=True)


        class TestModel(Model):
            class Meta:
                behaviors = (Unique,)
                reference_list = ('RelModel.single', 'RelModel.multiple',)
    """

    def _get_id(self):
        if hasattr(self.Model.Meta, 'uniqueness_identifier'):
            return self.Model.Meta.uniqueness_identifier
        else:
            return 'name'

    def _get_references(self):
        if hasattr(self.Model.Meta, 'reference_list'):
            return self.Model.Meta.reference_list
        else:
            return []

    def before_put(self, instance):
        key = instance.key.id()
        unique_prop = format_key_name(getattr(instance, self._get_id()))
        unique_key = ndb.Key(self.Model, unique_prop)
        # new entity
        if not key:
            if unique_key.get():
                raise UniqueError("%s.%s should be unique!" % (self.Model.__name__, self._get_id(),))
            else:
                instance.key = unique_key
        # updating instance, key exists
        else:
            # change in value of unique prop
            if key != unique_prop:
                # check if it already exists
                if unique_key.get():
                    raise UniqueError("%s.%s should be unique!" % (self.Model.__name__, self._get_id(),))
                # if it does not exist yet, replace key
                else:
                    # handle all children
                    for key in ndb.Query(ancestor=instance.key).iter(keys_only=True):
                        obj = key.get()
                        meta = obj.__class__
                        getval = lambda prop_name: getattr(obj, prop_name)
                        props = {prop_name: getval(prop_name) for prop_name in meta._properties if getval(prop_name)}
                        meta(parent=unique_key, **props).put()
                        key.delete()
                    # handle KeyProperty associations
                    refs = self._get_references()
                    for ref in refs:
                        model, prop_name = ref.split('.')
                        for key in ndb.Query(kind=model, filters=ndb.query.FilterNode(prop_name, '=', instance.key)).iter(keys_only=True):
                            obj = key.get()
                            getval = lambda prop_name: getattr(obj, prop_name)
                            if obj.__class__._properties[prop_name]._repeated:
                                lst = getval(prop_name)
                                idx = lst.index(instance.key)
                                lst[idx] = unique_key
                                setattr(obj, prop_name, lst)
                            else:
                                setattr(obj, prop_name, unique_key)
                    # [].index('bar')
                    instance.key.delete()  # delete key
                    instance.key = unique_key


class UniqueError(Exception):
    pass


def format_key_name(key_name):
    return str(key_name).replace(' ', '_').lower()


def model_factory(name):
    return type(name, (Model,), {})
