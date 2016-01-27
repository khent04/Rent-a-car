from ferris import Controller, route_with, messages
from app.models.car import Car
from app.models.user.user import User
from google.appengine.api import users
from google.appengine.ext import deferred
from ferris.core import mail
import json
import logging


class Cars(Controller):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        Model = Car
        Message = Car.message()


    @staticmethod
    def messaging_transform_function(entity, message, converters=None, only=None, exclude=None):
        return User.car_message(entity, message)

    @route_with('/api/cars/list', methods=['GET'])
    def api_lis(self):
        self.context['data'] = Car.query()

    @route_with('/api/vendor_cars/<vendor>', methods=['GET'])
    def api_vendor_cars(self, vendor):
        vendor = User.get(vendor, key_only=True)
        self.meta.Message = Car.full_message()
        self.meta.messaging_transform_function = Car.transform_message
        self.context['data'] = Car.list_by_vendor(vendor)

    @route_with('/api/cars/:<key>', methods=['GET'])
    def api_view(self, key):
        self.meta.Message = Car.full_message()
        self.meta.messaging_transform_function = Car.transform_message
        self.context['data'] = self.util.decode_key(key).get()

    @route_with('/api/cars/:<key>', methods=['PUT'])
    def api_update(self, key):
        params = json.loads(self.request.body)
        if 'seats' in params:
            if params['seats']:
                params['seats'] = int(params['seats'])
        else:
            params['seats'] = 0

        if 'trunk_capacity' in params:
            if params['trunk_capacity']:
                params['trunk_capacity'] = float(params['trunk_capacity'])
        else:
            params['trunk_capacity'] = 0.0

        if 'age' in params:
            if params['age']:
                params['age'] = int(params['age'])
        else:
            params['age'] = 0

        params['price'] = float(params['price'])
        params['location'] = params['location'].lower()

        car = self.util.decode_key(key).get()
        car.update(**params)
        return 200

    @route_with('/api/search/cars', methods=['POST'])
    def api_search(self):
        params = json.loads(self.request.body)
        self.meta.Message = Car.full_message()
        self.meta.messaging_transform_function = Car.transform_message
        data = Car.basic_search(params)
        if data:
            self.context['data'] = data
        else:
            return 200

    @route_with('/api/search/cars/top', methods=['POST'])
    def api_top(self):
        params = json.loads(self.request.body)
        self.meta.Message = Car.full_message()
        self.meta.messaging_transform_function = Car.transform_message
        data = Car.show_top_rated(params)
        if data:
            self.context['data'] = data
        else:
            return 200



    @route_with('/api/cars/upload/<vendor>', methods=['POST'])
    def api_upload(self, vendor):
        data = json.loads(self.request.body)
        for item in data:
            deferred.defer(async_upload_user, item, vendor)
        return 200

    @route_with('/api/delete/cars', methods=['PUT'])
    # we cannot get data in DELETE method, but we need to get
    # list of keys, so we'll be using put
    def api_delete(self):
        params = json.loads(self.request.body)
        map(lambda key: self.util.decode_key(key).delete(), params)
        return 200


def async_upload_user(item, vendor):
    if vendor:
        try:
            params = dict()
            params['seats'] = int(item['Seats'])
            params['car_model'] = item['Model']
            params['price'] = float(item['Price'])
            params['transmission'] = item['Transmission']
            params['availability'] = bool(item['Availability'])
            params['vendor'] = User.get(vendor, key_only=True)
            params['location'] = item['Location'].lower()
            Car.create(**params)
        except Exception as e:
            subject = 'Error while uploading cars'
            body = 'item={0}, error={1}:{2}'.format(item, e.__class__.__name__, e.message)
            mail.send(vendor, subject, body)
            logging.info("error while uploading cars." + str(e))
