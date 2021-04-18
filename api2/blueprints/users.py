from flask import jsonify, request, abort
from werkzeug.security import generate_password_hash

from api2 import db
from api2.blueprints import bp_api
from api2.models import User
from api2.models.users import UserSchema


@bp_api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    schema = UserSchema(many=True)
    return jsonify(schema.dump(users))


@bp_api.route('/users/<int:user_id>/get', methods=['GET'])
def get_user(user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return abort(404, f'No such {user_id} user_id')

    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))


@bp_api.route('/users/<int:user_id>/update', methods=['PATCH'])
def user_update(user_id):
    user = User.query.filter(User.id == user_id).first()
    data = request.json

    if not user:
        return abort(404, f'No such {user_id} user_id')

    user.query.update(data)

    db.session.add(user)
    db.session.commit()

    user_schema = UserSchema()
    return user_schema.jsonify(user)


@bp_api.route('/users/<int:user_id>/delete', methods=['DELETE'])
def user_delete(user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return abort(404, f'No such {user_id} user_id')

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User with {user_id} id was deleted'})


@bp_api.route('/users/create', methods=['POST'])
def user_create():
    data = request.json
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password_hash']),
        email=data['email']
    )

    db.session.add(user)
    db.session.commit()

    schema = UserSchema()
    return schema.jsonify(user)
