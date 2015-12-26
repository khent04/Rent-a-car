from google.appengine.api import users
from ferris import Controller, route_with
from app.misc.auth import only
from app.models.user.user import User
from app.services.user_svc import UserSvc
from protorpc import protojson
# import logging


class Main(Controller):
    print "\n\n\n\n\n===============\n\n\n\n"

    @route_with(template='/admin')
    @only("=", "Admin")
    def admin(self):
        print "**********"
        return 200
        # active_user = UserSvc.get_current_user()
        # user = User.transform_message(active_user, User.message())
        # self.meta.view.template_name = 'angular/admin-index.html'
        # self.context['active_user'] = protojson.encode_message(user)
        # self.context['logout_url'] = users.create_logout_url('/')


    @route_with(template='/admin2')
    def index(self):
        active_user = UserSvc.get_current_user()
        # user = User.transform_message(active_user, User.message())
        self.meta.view.template_name = 'angular/admin-index.html'
        self.context['data'] = active_user
        self.context['active_user'] = self.context['data']
        self.context['logout_url'] = users.create_logout_url('/')
