from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from api2 import db
from api2.blueprints import posts_api
from api2.models import Post
from api2.models.posts import PostSchema
from api2.perm_decorators import admin_required


@posts_api.route('/', methods=['GET'])
@jwt_required()
def get_list():
    posts = db.session.query(Post)
    post_schema = PostSchema(many=True)

    priority = request.args.get('priority')
    post_type = request.args.get('type')

    if post_type:
        posts = posts.filter(Post.type == post_type)
    if priority:
        posts = posts.filter(Post.priority == priority)

    return jsonify(post_schema.dump(posts))


@posts_api.route('/get/<int:post_id>', methods=['GET'])
@jwt_required()
def get_one_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if not post:
        return abort(404, description='No post with such id')

    post_schema = PostSchema()
    return post_schema.dump(post), 200


@posts_api.route('/update/<int:post_id>', methods=['PATCH'])
@jwt_required()
def update_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return abort(404, description='No post with such id')

    post_schema = PostSchema()
    json_data = request.json
    try:
        data = post_schema.load(json_data)
    except ValidationError:
        return abort(400, description='Invalid data type. Expected "string".')

    post.query.update(data)
    db.session.add(post)
    db.session.commit()
    return post_schema.dump(post)


@posts_api.route('/delete/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return abort(404, description='No post with such id')

    db.session.delete(post)
    db.session.commit()

    return {'message': f'Post with {post_id} id was deleted'}, 204


@posts_api.route('/create', methods=['POST'])
@jwt_required()
def add_post():
    json_data = request.json

    post_schema = PostSchema()
    try:
        data = post_schema.load(json_data)
    except ValidationError:
        return abort(400, description='Invalid data type one of a fields.')

    data['user_id'] = current_user.id
    post = Post(**data)

    db.session.add(post)
    db.session.commit()
    return post_schema.dump(post), 201


@posts_api.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def posts_of_user(user_id):
    post_schema = PostSchema(many=True)
    posts = Post.query.filter(Post.user_id == user_id)

    priority = request.args.get('priority')
    post_type = request.args.get('type')

    if post_type:
        posts = posts.filter(Post.type == post_type)
    if priority:
        posts = posts.filter(Post.priority == priority)

    return jsonify(post_schema.dump(posts))




@posts_api.route('/testing', methods=['GET'])
@jwt_required()
@admin_required
def testing():
    return {"mes": "Retrieve"}


