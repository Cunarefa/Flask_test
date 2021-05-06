from functools import wraps
from flask import abort, g


def admin_required(fun):
    @wraps(fun)
    def decorator(*args, **kwargs):
        if not g.user or g.user.role != "ADMIN":
            abort(403)
        return fun(*args, **kwargs)

    return decorator
