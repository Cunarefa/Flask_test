from flask import request, jsonify

from api2 import db
from api2.blueprints import bp_api
from api2.models import Post
from api2.models.posts import PostSchema


@bp_api.route('/posts', methods=['GET'])
def get_list():
    posts = Post.query.all()
    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts)
    return jsonify(output)


@bp_api.route('/post/<int:post_id>/get', methods=['GET'])
def get_one_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify({'error': 'No such post'})

    post_schema = PostSchema()
    output = post_schema.dump(post)
    return jsonify(output)


@bp_api.route('/post/<int:post_id>/update', methods=['PATCH'])
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    data = request.json

    if not post:
        return jsonify({'error': 'No such post'})

    post.title = data['title']
    db.session.commit()

    post_schema = PostSchema()
    return post_schema.jsonify(post)


@bp_api.route('/post/<int:post_id>/delete', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return jsonify({'error': 'No such post'})

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': f'Post with {post_id} id was deleted'})


@bp_api.route('/post/create', methods=['POST'])
def add_post():
    data = request.json
    post = Post(
        title=data['title']
    )
    db.session.add(post)
    db.session.commit()

    post_schema = PostSchema()
    return post_schema.jsonify(post)
