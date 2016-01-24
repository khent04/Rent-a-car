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

    @route_with('/api/cars/list', methods=['GET'])
    def api_lis(self):
        self.context['data'] = Car.query()

    @route_with('/api/vendor_cars/<vendor>', methods=['GET'])
    def api_vendor_cars(self, vendor):
        vendor = User.get(vendor, key_only=True)
        self.context['data'] = Car.list_by_vendor(vendor)

    @route_with('/api/cars/:<key>', methods=['GET'])
    def api_view(self, key):
        self.context['data'] = self.util.decode_key(key).get()

    @route_with('/api/cars/upload/<vendor>', methods=['POST'])
    def api_upload(self, vendor):
        data = json.loads(self.request.body)
        for item in data:
            deferred.defer(async_upload_user, item, vendor)
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
            Car.create(**params)
        except Exception as e:
            subject = 'Error while uploading cars'
            body = 'item={0}, error={1}:{2}'.format(item, e.__class__.__name__, e.message)
            mail.send(vendor, subject, body)
            logging.info("error while uploading cars." + str(e))
