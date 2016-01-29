from google.appengine.api import users
from ferris import Controller, route_with, messages, add_authorizations, route
from app.models.user.user import User
from app.services.user_svc import UserSvc
from protorpc import protojson
import logging


class Main(Controller):

    @route_with(template='/')
    def index(self):
        active_user = User.get("kenneth.estrella@cloudsherpas.com")
        print "\n\n\n!!!!!!!!-->>>>>>%s\n\n" % active_user
        self.context['active_user'] = 'null'
        self.meta.view.template_name = 'angular/app-index.html'

    @route
    def login_admin(self):
        if not users.get_current_user():
            self.context['data'] = "%s"%users.create_login_url('/admin')
        else:
            return 403

    @route_with(template='/admin')
    def admin(self):
        print User.get(users.get_current_user())
        if users.is_current_user_admin():
            self.context['data'] = users.get_current_user()
            self.context['logout_url'] = users.create_logout_url('/')
            self.meta.view.template_name = 'angular/admin-index.html'
        else:
            return self.redirect(self.uri(action="login_admin"))
