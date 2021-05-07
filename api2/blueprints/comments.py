from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from api2 import db
from api2.blueprints import comment_api
from api2.models import Post
from api2.models.comments import CommentSchema, Comment
from api2.perm_decorators import roles_required


@comment_api.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
@roles_required('Editor')
def add_comment(post_id):
    json_data = request.json
    comment_schema = CommentSchema()

    try:
        data = comment_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    data['author_id'] = current_user.id
    comment = Comment(**data)
    db.session.add(comment)
    db.session.commit()

    return {"message": f"You have just commented the post with {post_id} id."}


@comment_api.route('/posts/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def post_comments_list(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    comments = post.comments
    schema = CommentSchema(many=True)

    return jsonify(schema.dump(comments))


@comment_api.route('comments/<int:comment_id>', methods=["DELETE"])
@jwt_required()
@roles_required('Editor')
def delete_comment(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id)

    if not comment:
        return abort(404, description='No comment with such id')

    db.session.delete(comment)
    db.session.commit()
    return {"message": f"Comment with {comment_id} id was deleted."}


@comment_api.route('/comments/<int:comment_id>', methods=["PATCH"])
@jwt_required()
@roles_required('Editor')
def update_comment(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()
    comment_schema = CommentSchema()
    json_data = request.json

    try:
        data = comment_schema.load(json_data)
    except ValidationError:
        return abort(400, description='Invalid data type. Expected "string".')

    comment.query.update(data)
    db.session.add(comment)
    db.session.commit()
    return comment_schema.dump(comment)
