from app.models.user.user import User
from ferris import Controller, route_with, messages
from google.appengine.api import users
import json


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

    @route_with('/api/users', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        self.context["data"] = User.create(**params)

    @route_with('/api/users/<email>', methods=['PUT', 'POST'])
    def api_update(self, email):
        user = User.get(email, key_only=False)
        # id is the email, remember we made the email unique id
        if not user:
            return 404
        params = json.loads(self.request.body)
        user.update(**params)
        return 200

    @route_with('/api/users', methods=['GET'])
    def api_list(self):
        self.context['data'] = User.query()
