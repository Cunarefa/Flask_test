from flask import jsonify, request, abort, make_response

from api2 import db
from api2.blueprints import bp_api
from api2.models import User
from api2.models.users import UserSchema


@bp_api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    schema = UserSchema(many=True)
    output = schema.dump(users)
    return jsonify(output)


@bp_api.route('/user/<int:user_id>/get', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(user_id).first()
    if not user:
        return abort(404, description='No such a user')

    schema = UserSchema()
    return jsonify(schema.dump(user))


@bp_api.route('/user/<int:user_id>/update', methods=['PATCH'])
def user_update(user_id):
    user = User.query.filter(User.id == user_id).first()
    data = request.json
    if not user:
        return abort(404, description='No such a user')

    user.username = data['username']
    user.email = data['email']

    db.session.add(user)
    db.session.commit()

    schema = UserSchema()
    return schema.jsonify(user)


@bp_api.route('/user/<int:user_id>/delete', methods=['DELETE'])
def user_delete(user_id):
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': f'No such {user_id} user'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User with {user_id} id was deleted'})


@bp_api.route('/user/create', methods=['POST'])
def user_create():
    data = request.json
    user = User(
        username=data['username'],
        email=data['email']
    )

    db.session.add(user)
    db.session.commit()

    schema = UserSchema()
    return make_response(jsonify({'data': schema.dump(user)}, 201))
