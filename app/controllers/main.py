from google.appengine.api import users
from ferris import Controller, route_with, messages, add_authorizations
from app.misc.auth import only
from app.models.user.user import User
from app.services.user_svc import UserSvc
from protorpc import protojson
import logging



class Main(Controller):

    @route_with(template='/')
    def index(self):
        active_user = UserSvc.get_current_user()
        # if active_user and active_user._class_name() == 'Vendor':
        #     logging.info('user is Vendor')
        # elif active_user and active_user._class_name() == 'Renter':
        #     logging.info('User is Renter')
        # else:
        #     logging.info('Visitor')
        self.context['active_user'] = 'null'
        self.meta.view.template_name = 'angular/app-index.html'

    # @route_with(template='/register')
    # def register(self):


    #     if not active_user:
    #         active_user = UserSvc.create_selling_partner()

    #     if active_user._class_name() == 'SellingPartner':
    #         logging.info('is selling selling_partner!!')
    #         user = SellingPartner.to_message(active_user, SellingPartner.full_message())
    #     else:
    #         user = User.transform_message(active_user, User.message())

    #     VisitLog.create(log=UserSvc.get_current_user(key_only=True))
    #     self.meta.view.template_name = 'angular/app-index.html'
    #     self.context['active_user'] = protojson.encode_message(user)
    #     self.context['logout_url'] = users.create_logout_url('/')

    @route_with(template='/admin')
    @only("=", "Admin")
    def admin(self):

        self.meta.view.template_name = 'angular/admin-index.html'
        self.context['data'] = active_user
        self.context['active_user'] = self.context['data']
        self.context['logout_url'] = users.create_logout_url('/')
