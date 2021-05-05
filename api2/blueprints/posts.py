from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import func, desc

from api2 import db
from api2.blueprints import bp_api
from api2.models import Post
from api2.models.posts import PostSchema


@bp_api.route('/posts', methods=['GET'])
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


@bp_api.route('/posts/get/<int:post_id>', methods=['GET'])
@jwt_required()
def get_one_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if not post:
        return abort(404, description='No post with such id')

    post_schema = PostSchema()
    return post_schema.dump(post), 200


@bp_api.route('/posts/update/<int:post_id>', methods=['PATCH'])
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


@bp_api.route('/posts/delete/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return abort(404, description='No post with such id')

    db.session.delete(post)
    db.session.commit()

    return {'message': f'Post with {post_id} id was deleted'}, 204


@bp_api.route('/posts/create', methods=['POST'])
@jwt_required()
def add_post():
    json_data = request.json

    post_schema = PostSchema()
    try:
        data = post_schema.load(json_data)
    except ValidationError:
        return abort(400, description='Invalid data type one of a fields.')

    post = Post(
        title=data['title'],
        description=data['description'],
        type=data['type'],
        priority=data['priority']
    )

    db.session.add(post)
    db.session.commit()
    return post_schema.dump(post), 201


@bp_api.route('/posts/user/<int:user_id>', methods=['GET'])
@jwt_required()
def posts_of_user(user_id):
    post_schema = PostSchema(many=True)
    posts = Post.query.filter(Post.user_id == user_id).all()

    priority = request.args.get('priority')
    post_type = request.args.get('type')

    if post_type:
        posts = posts.filter(Post.type == post_type)
    if priority:
        posts = posts.filter(Post.priority == priority)

    return jsonify(post_schema.dump(posts))

