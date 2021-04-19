from flask import request, jsonify, abort, make_response
from marshmallow import ValidationError

from api2 import db
from api2.blueprints import bp_api
from api2.models import Post
from api2.models.posts import PostSchema


@bp_api.route('/posts', methods=['GET'])
def get_list():
    posts = Post.query.all()
    post_schema = PostSchema(many=True)
    return jsonify(post_schema.dump(posts))


@bp_api.route('/posts/<int:post_id>/get', methods=['GET'])
def get_one_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if not post:
        return abort(404, description='No post with such id')

    post_schema = PostSchema()
    return jsonify(post_schema.dump(post))


@bp_api.route('/posts/<int:post_id>/update', methods=['PATCH'])
def update_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return abort(404, description='No post with such id')

    post_schema = PostSchema()

    json_data = request.json
    data = post_schema.load(json_data)

    post.query.update(data)

    db.session.add(post)
    db.session.commit()

    return jsonify(post_schema.dump(post))


@bp_api.route('/posts/<int:post_id>/delete', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return abort(404, description='No post with such id')

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': f'Post with {post_id} id was deleted'})


@bp_api.route('/posts/create', methods=['POST'])
def add_post():
    data = request.json
    post = Post(
        title=data['title'],
        description=data['description'],
        type=data['type'],
        priority=data['priority']
    )

    db.session.add(post)
    db.session.commit()

    post_schema = PostSchema()
    return make_response(post_schema.dump(post), 201)
