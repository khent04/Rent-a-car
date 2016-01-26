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
        Message = Reservation.message()

    @staticmethod
    def messaging_transform_function(entity, message, converters=None, only=None, exclude=None):
        return User.car_message(entity, message)

    @route_with('/api/reservations/:<key>', methods=['POST'])
    def api_reserve(self, key):
        params = json.loads(self.request.body)
        params['car'] = self.util.decode_key(key)
        params['renter'] = User.get(params['renter'], key_only=True)
        params['pickup_date'] = datetime.datetime.strptime(params['pickup_date'].split('T')[0], '%Y-%m-%d')
        params['dropoff_date'] = datetime.datetime.strptime(params['dropoff_date'].split('T')[0], '%Y-%m-%d')
        params['request_code'] = code_generator()
        params['amount'] = 12.12
        Reservation.create(**params)
        return 200

    @route_with('/api/reservations/pending', methods=['GET'])
    def api_list(self):
        lis = Reservation.list(False)
        if lis:
            self.meta.Message = Reservation.full_message()
            self.meta.messaging_transform_function = Reservation.transform_message
            self.context['data'] = lis
        else:
            return 200

    @route_with('/api/reservations/:<key>', methods=['GET'])
    def api_get(self, key):
        self.meta.Message = Reservation.full_message()
        self.meta.messaging_transform_function = Reservation.transform_message
        self.context['data'] = self.util.decode_key(key).get()

    @route_with('/api/reservations/:<key>', methods=['PUT'])
    def api_update(self, key):
        params = json.loads(self.request.body)
        request = self.util.decode_key(key).get()
        request.update(**params)
        car = request.car.get()
        vendor = car.vendor.get()
        renter = request.renter.get()
        deferred.defer(send_mail, car, vendor, renter, request)
        return 200

    @route_with('/api/reservations/batch_process/<action>', methods=['POST'])
    def api_batch_process(self, action):
        request_list = json.loads(self.request.body)
        if action == "approved":
            args = dict(approved=True, rejected=False)
        if action == "rejected":
            args = dict(approved=False, rejected=True)

        map(lambda key: self.util.decode_key(key).get().update(**args), request_list)
        for key in request_list:
            request = self.util.decode_key(key).get()
            car = request.car.get()
            vendor = car.vendor.get()
            renter = request.renter.get()
            deferred.defer(send_mail, car, vendor, renter, request)
        return 200

    # for renter rentals
    @route_with('/api/rentals/<email>', methods=['GET'])
    def api_rentals_list(self, email):
        renter = User.get(email, key_only=True)
        data =  Reservation.rentals(renter).fetch()
        self.meta.Message = Reservation.full_message()
        self.meta.messaging_transform_function = Reservation.transform_message
        self.context['data'] = data


def code_generator():
    return str(uuid.uuid4())[0:8]

def send_mail(car, vendor, renter, request):
    try:
        recipient = renter.email
        logging.info("Sending email to %s"%recipient)
        subject = "CarE Rental Booking Status"
        template = """
        <table cellpadding="5">
            <thead>
            <tr>
                <td>Transaction Code</td>
                <td>Car</td>
                <td>Vendor</td>
                <td>Price</td>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
            </tbody>
        </table>
        <br>
        Here is the contact details of the vendor:<br>
        email: %s<br>
        contact number: %s <br>
        """ % (request.request_code, car.car_model, vendor.company, request.amount, vendor.email, vendor.contact_number)
        body = """Hi %s, <br><br>
                      Your booking request was %s. <br>
                      Here are the details of transaction: <br><br>
                      %s""" % (renter.first_name, "approved" if request.approved else "rejected", template)
        mail.send(recipient, subject, body)
        print body
    except Exception, e:
        logging.info("########-------->>>>>>")
        logging.info(str(e))
