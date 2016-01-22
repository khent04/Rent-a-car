from ferris import Controller, route_with, messages
from app.models.car import Car
from app.models.user.user import User
from google.appengine.api import users
from google.appengine.ext import deferred
import json



class Cars(Controller):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        Model = Car

    # @route_with('/api/cars/<vendor>', methods=['POST'])
    # def api_add(self, vendor):
    #     params = json.loads(self.request.body)
    #     params['vendor'] = User.get(vendor, key_only=True)
    #     self.context["data"] = Car.create(**params)

    @route_with('/api/cars/list', methods=['GET'])
    def api_lis(self):
        self.context['data'] = Car.query()

    @route_with('/api/vendor_cars/<vendor>', methods=['GET'])
    def api_vendor_cars(self, vendor):
        vendor = User.get(vendor, key_only=True)
        self.context['data'] = Car.list_by_vendor(vendor)
        # return 200

    @route_with('/api/cars/upload/<vendor>', methods=['POST'])
    def api_upload(self, vendor):
        vendor = User.get(vendor, key_only=True)
        data = json.loads(self.request.body)
        for item in data:
            deferred.defer(async_upload_user, item, vendor)
        return 200

def async_upload_user(item, vendor):
    params = dict()
    params['seats'] = int(item['Seats'])
    params['car_model'] = item['Model']
    params['price'] = float(item['Price'])
    params['transmission'] = item['Transmission']
    params['availability'] = bool(item['Availability'])
    params['vendor'] = vendor
    Car.create(**params)
