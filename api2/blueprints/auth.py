from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from api2 import db
from api2.blueprints import bp_auth
from api2.models import User
from api2.models.users import UserSchema


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username', None)
    password = request.args.get('password', None)

    # if username != "cunarefa" or password != 123:
    #     return jsonify({'login': False}), 401
    # user = User.query.filter(User.username == username).one()
    # token = user.create_jwt_token(identity=username)
    # return jsonify({"token": token})

    # if username and password:

    user = User.query.filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        token = user.create_jwt_token(identity=username)
        return jsonify({"token": token})
    return make_response('Username or password is incorrect!', 401)


@bp_auth.route('/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(**json_data)
    db.session.add(user)
    db.session.commit()
    # login(user)
    return jsonify({"message": "User was created"})
