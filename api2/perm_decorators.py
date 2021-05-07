from functools import wraps
from flask import abort
from flask_jwt_extended import current_user

from api2.models.enums import Role


class roles_required:

    def __init__(self, role):
        self.role = role

    def __call__(self, fun):
        @wraps(fun)
        def decorator(*args, **kwargs):
            if not current_user or (current_user.role != Role.ADMIN and current_user.role.value != self.role):
                abort(403)
            return fun(*args, **kwargs)

        return decorator


