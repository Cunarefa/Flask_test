from flask import abort, jsonify
from flask_jwt_extended import jwt_required

from api2 import db
from api2.blueprints import user_api
from api2.models import User

from api2.models.enums import Role
from api2.models.users import UserRegisterSchema
from api2.perm_decorators import roles_required


@user_api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@roles_required(Role.ADMIN)
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    if user.deleted:
        abort(404)
    user.deleted = True
    db.session.commit()
    return f'{user.username} user was deleted', 200


@user_api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@roles_required(Role.ADMIN)
def get_user(user_id):
    schema = UserRegisterSchema()
    user = User.query.filter(User.id == user_id).first_or_404()
    if user.deleted:
        abort(404)
    return schema.dump(user)


@user_api.route('/users', methods=['GET'])
@jwt_required()
@roles_required(Role.ADMIN)
def get_all_users():
    schema = UserRegisterSchema(many=True)
    users = User.query.filter(User.deleted in False).all()
    return jsonify(schema.dump(users))
