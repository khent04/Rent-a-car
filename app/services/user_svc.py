from google.appengine.api import users
from app.models.user.user import User

class UserSvc:

    @staticmethod
    def get_current_user(key_only=False):
        user = users.get_current_user()
        if user:
            return User.get(user.email().lower(), key_only=key_only)

    @staticmethod
    def generate_logout_url():
        return users.create_logout_url('/')
