from app.models.user.user import User
from app.models.user.renter import Renter
from app.models.user.vendor import Vendor
from ferris import Controller, route_with, messages, route
from google.appengine.api import users
from app.models.media_uploader import MediaUploader
from google.appengine.ext import deferred
from ferris.core import mail
import logging
import StringIO
import xlsxwriter
import json

class Users(Controller):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        Model = User
        Message = User.message()

    @staticmethod
    def messaging_transform_function(entity, message, converters=None, only=None, exclude=None):
        return User.car_message(entity, message)

    @route_with('/api/users/<role>', methods=['POST'])
    def api_add(self, role):
        params = json.loads(self.request.body)
        if_exist = params['email']
        if User.get(if_exist):
            self.context["data"] = User.get(if_exist)
        else:
            if role == "Renter":
                self.context["data"] = Renter.create(**params)
            if role == "Vendor":
                self.context["data"] = Vendor.create(**params)

    @route_with('/api/users/<email>', methods=['PUT'])
    def api_update(self, email):
        user = User.get(email, key_only=False)
        # id is the email, remember we made the email unique id
        if not user:
            return 404
        params = json.loads(self.request.body)
        if 'user_type' not in params:
            params['credentials'] = map(lambda x: self.util.decode_key(str(x).strip()), params['credentials'])
        else:
            del params['user_type']
        user.update(**params)
        return 200

    @route_with('/api/users/<email>', methods=['GET'])
    def api_get(self, email):
        user = User.get(email, key_only=False)
        if user._class_name() == 'Renter':
            self.meta.Message = Renter.full_message()
            self.meta.messaging_transform_function = Renter.transform_message
        else:
            return self.util.stringify_json(User.get(email))
        self.context['data'] = user

    @route_with('/api/users', methods=['GET'])
    def api_list(self):
        self.context['data'] = User.query()

    @route
    def xlsx(self):
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        # Write some test data.
        worksheet.write('A1', 'Seats')
        worksheet.write('B1', 'Model')
        worksheet.write('C1', 'Price')
        worksheet.write('D1', 'Transmission')
        worksheet.write('E1', 'Availability')
        worksheet.data_validation('D2:D500', {'validate': 'list',
                                 'source': ['Automatic', 'Manual'],
                                 })
        worksheet.data_validation('E2:E500', {'validate': 'list',
                                 'source': ['Available', 'Not Available'],
                                 })
        workbook.close()
        # Rewind the buffer.
        output.seek(0)
        self.response.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.response.content_disposition = 'attachment; filename=carE_Rentals_template.xlsx'
        data = output.getvalue()
        self.response.write(data)
        return self.response


    @route_with('/api/vendors', methods=['GET'])
    def api_vendor_request(self):
        return self.util.stringify_json(Vendor.vendor_request())

    @route_with('/api/vendors', methods=['PUT'])
    def api_vendor_approve(self):
        activates = {"activated": True}
        params = json.loads(self.request.body)
        map(lambda x: User.get(x).update(**activates), params)
        map(lambda x: deferred.defer(send_mail, x), params)
        return 200


def send_mail(user):
    logging.info("Sending email to %s"%user)
    name = User.get(user).first_name
    subject = "CarE Rental: Account activated!"
    body = "Welcome %s to CarE Rental. You can now upload cars for rent."%name
    mail.send(user, subject, body)
