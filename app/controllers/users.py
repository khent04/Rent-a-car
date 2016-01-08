from app.models.user.user import User
from app.models.user.renter import Renter
from app.models.user.vendor import Vendor
from ferris import Controller, route_with, messages, route
from google.appengine.api import users
import json
from app.models.media_uploader import MediaUploader
from google.appengine.ext import deferred
# from google.appengine.api import mail
from ferris.core import mail
import logging
import StringIO
import xlsxwriter


class Users(Controller):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        Model = User

    # sample only
    @route_with('/api/users/sample')
    def api_create_sample(self):
        params = {
            "email": users.get_current_user().email(),
            "contact_number": "9051873584",
            "first_name": "ken",
            "last_name": "estrella",
            }
        self.context["data"] = User.create(**params)

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



    @route_with('/api/users/<email>', methods=['PUT', 'POST'])
    def api_update(self, email):
        user = User.get(email, key_only=False)
        # id is the email, remember we made the email unique id
        if not user:
            return 404
        params = json.loads(self.request.body)
        params['credentials'] = map(lambda x: self.util.decode_key(str(x).strip()), params['credentials'])
        user.update(**params)
        return 200

    @route_with('/api/users/<email>', methods=['GET'])
    def api_get(self, email):
        # self.context['data'] = User.get(email)
        return self.util.stringify_json(User.get(email))

    @route_with('/api/users', methods=['GET'])
    def api_list(self):
        self.context['data'] = User.query()

    @route_with('/api/users/ken', methods=['GET'])
    def ken(self):
        return 200

    @route
    def xlsx(self):
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        # Write some test data.
        # worksheet.write(0, 0, 'Hello, world!')
        worksheet.data_validation('A4', {'validate': 'list',
                                 'source': ['open', 'high', 'close'],
                                 })
        workbook.close()
        # Rewind the buffer.
        output.seek(0)
        self.response.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.response.content_disposition = 'attachment; filename=test.xlsx'
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
