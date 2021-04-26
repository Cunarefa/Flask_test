from flask import request, make_response, abort
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api2 import db
from api2.blueprints import bp_auth
from api2.models import User
from api2.models.users import UserLoginSchema, UserRegisterSchema


@bp_auth.route('/register', methods=['POST'])
def register():
    json_data = request.json
    post_schema = UserRegisterSchema()

    try:
        data = post_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    data['password'] = generate_password_hash(data['password'])
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    token = user.create_jwt_token()
    return {"token": token}


@bp_auth.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']

    user_schema = UserLoginSchema()
    try:
        user_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    user = User.query.filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        token = user.create_jwt_token()
        return {"token": token}
    return make_response(f"Couldn't verify!", 401)
