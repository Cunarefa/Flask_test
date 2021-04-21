from flask import request, abort, jsonify
from marshmallow import ValidationError

from api2 import db
from api2.blueprints import bp_api
from api2.models import Post
from api2.models.posts import PostSchema


@bp_api.route('/posts', methods=['GET'])
def get_list():
    posts = Post.query.all()
    post_schema = PostSchema(many=True)

    if request.args:
        priority = request.args.get('priority')
        post_type = request.args.get('type')

        querys = []
        if post_type:
            querys.append(Post.type == post_type)
        elif priority:
            querys.append(Post.priority == priority)
        priority_filter = Post.query.filter(*querys)
        return jsonify(post_schema.dump(priority_filter))

    return jsonify(post_schema.dump(posts))


@bp_api.route('/posts/<int:post_id>/get', methods=['GET'])
def get_one_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if not post:
        return abort(404, description='No post with such id')

    post_schema = PostSchema()
    return post_schema.dump(post)


@bp_api.route('/posts/<int:post_id>/update', methods=['PATCH'])
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


@bp_api.route('/posts/<int:post_id>/delete', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return abort(404, description='No post with such id')

    db.session.delete(post)
    db.session.commit()

    return {'message': f'Post with {post_id} id was deleted'}, 204


@bp_api.route('/posts/create', methods=['POST'])
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
