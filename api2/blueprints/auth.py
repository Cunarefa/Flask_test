from flask import request, make_response, abort
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api2 import db
from api2.blueprints import auth_api
from api2.models import User
from api2.models.users import UserLoginSchema, UserRegisterSchema


@auth_api.route('/register', methods=['POST'])
def register():
    json_data = request.json
    user_schema = UserRegisterSchema()

    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    data['password'] = generate_password_hash(data['password'])
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    token = user.create_jwt_token()
    return {"token": token, "user": user_schema.dump(user)}


@auth_api.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()

    user_schema = UserLoginSchema()
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    username = data['username']
    password = data['password']

    user = User.query.filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        token = user.create_jwt_token()
        return {"token": token, "user": user_schema.dump(user)}
    return make_response(f"Couldn't verify!", 401)

