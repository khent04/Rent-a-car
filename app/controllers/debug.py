from ferris import route_with, BasicModel, messages
from app.models.user.admin import Admin
from app.controllers.base_controller import CarERentalController
from ferris import Controller


class Debug(CarERentalController):
    class Meta:
        prefixes = ("api",)
        components = (messages.Messaging,)
        Model = BasicModel

    @route_with("/api/debug/create_admin/<email>")
    def api_init_cet_users(self, email):
        self.init_cet_users(email)
        return 200

    def init_cet_users(self, email):
        Admin.create(email=email)
