from flask import request, jsonify, make_response, abort
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api2 import db
from api2.blueprints import bp_auth
from api2.models import User
from api2.models.users import UserSchema


@bp_auth.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    user = User.query.filter(User.username == auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = user.create_jwt_token()
        return {"token": token}
    return make_response(f"Couldn't verify!", 401)


@bp_auth.route('/register', methods=['POST'])
def register():
    json_data = request.json
    post_schema = UserSchema()

    try:
        data = post_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    generate_password_hash(data['password'])
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    return login(user)
