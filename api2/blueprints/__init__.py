from flask import Blueprint

posts_api = Blueprint('posts_api', __name__)
auth_api = Blueprint('auth_api', __name__)
like_api = Blueprint('like_api', __name__)
comment_api = Blueprint('comment_api', __name__)

from api2.blueprints import posts, auth, likes, comments
