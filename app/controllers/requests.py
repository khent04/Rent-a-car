from app.models.user.user import User
from ferris import Controller, route_with, messages
from google.appengine.api import users
import json

class Requests(Controller):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        Model = User

    # sample only
    @route_with('/api/requests', methods=['POST', 'GET'])
    def api_create_sample(self):
        params = json.loads(self.request.body)
        return 200
