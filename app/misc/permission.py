# from app.models.user import User, get_permission_level
from app.services.user_svc import UserSvc


class Permission:
    @staticmethod
    def current_user_is(comparator, role):
        user = UserSvc.get_current_user()
        current_user_role = user._class_name() if user else 'not logged in'
        import logging
        logging.info(current_user_role)
        if comparator == '=':
            return get_permission_level(role) == get_permission_level(current_user_role)
        if comparator == '>':
            return get_permission_level(role) < get_permission_level(current_user_role)
        if comparator == '<':
            return get_permission_level(role) > get_permission_level(current_user_role)
        if comparator == '>=':
            return get_permission_level(role) <= get_permission_level(current_user_role)
        if comparator == '<=':
            return get_permission_level(role) >= get_permission_level(current_user_role)
        if comparator == '!=':
            return get_permission_level(role) != get_permission_level(current_user_role)
        if comparator == 'in':
            role_list = role.split(",")
            for individual_role in role_list:
                if get_permission_level(individual_role) == get_permission_level(current_user_role):
                    return True
            return False


def get_permission_level(role):
    if role == "Renter":
        return 10
    elif role == "Vendor":
        return 20
    elif role == "Admin":
        return 100
    else:
        return 0
