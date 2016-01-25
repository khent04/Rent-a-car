from ferris import Controller, route_with, messages
from app.models.car import Car
from app.models.reservation import Reservation
from app.models.user.user import User
from google.appengine.api import users
from google.appengine.ext import deferred
from ferris.core import mail
import json
import logging
import datetime
import uuid


class Reservations(Controller):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        Model = Reservation

    @route_with('/api/reservations/<key>', methods=['POST'])
    def api_reserve(self, key):
        params = json.loads(self.request.body)
        print "#################"
        params['car'] = self.util.decode_key(key)
        params['renter'] = User.get(params['renter'], key_only=True)
        params['pickup_date'] = datetime.datetime.strptime(params['pickup_date'].split('T')[0], '%Y-%m-%d')
        params['dropoff_date'] = datetime.datetime.strptime(params['dropoff_date'].split('T')[0], '%Y-%m-%d')
        params['request_code'] = code_generator()
        params['amount'] = 12.12
        print params
        Reservation.create(**params)
        return 200


def code_generator():
    return str(uuid.uuid4())[0:8]
