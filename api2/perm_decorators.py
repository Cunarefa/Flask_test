from functools import wraps
from flask import abort
from flask_jwt_extended import current_user

from api2.models.enums import Role


def roles_required(role):
    def decorator(fun):
        @wraps(fun)
        def decorated(*args, **kwargs):
            if not current_user or (current_user.role != Role.ADMIN and current_user.role != role):
                abort(403)
            return fun(*args, **kwargs)
        return decorated
    return decorator
