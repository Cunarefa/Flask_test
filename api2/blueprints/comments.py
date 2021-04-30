from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from api2 import db
from api2.blueprints import comment_api
from api2.models import Post
from api2.models.comments import CommentSchema, Comment


@comment_api.route('/add/onPost/<int:post_id>', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    json_data = request.json
    comment_schema = CommentSchema()

    try:
        data = comment_schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    content = data['content']
    post = Post.query.filter_by(id=post_id).first_or_404()
    current_user.comment_post(post, content)
    db.session.commit()

    return {"message": f"You have just commented the post with {post_id} id."}


@comment_api.route('/all/inPost/<int:post_id>', methods=['GET'])
@jwt_required()
def post_comments_list(post_id):
    comments = Comment.query.filter(Comment.post_id == post_id)
    schema = CommentSchema(many=True)

    return jsonify(schema.dump(comments))


@comment_api.route('/delete/comment/<int:comment_id>/fromPost/<int:post_id>', methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id, post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()

    if not current_user.has_commented(post):
        return abort(400, {"message": "You didn't comment this post"})

    current_user.delete_comment(post, comment_id)
    db.session.commit()
    return {"message": f"Comment with {comment_id} id was deleted."}


@comment_api.route('/update/<int:comment_id>', methods=["PATCH"])
@jwt_required()
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
