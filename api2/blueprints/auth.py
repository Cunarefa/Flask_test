from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash

from api2.blueprints import bp_auth
from api2.models import User


@bp_auth.route('/login', methods=['GET', 'POST'])
def login_page():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username and password:
        user = User.query.filter(User.username == username).first()
        if check_password_hash(user.password_hash, password):
            token = user.create_jwt_token(identity=username)
            return jsonify({"token": token})
    return make_response('Username or password is incorrect!', 401)
