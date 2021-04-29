import json

from flask import request, abort, jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from api2 import db
from api2.blueprints import comment_api
from api2.models import Post
from api2.models.comments import CommentSchema, Comment


@comment_api.route('/comments/post/<int:post_id>', methods=['POST'])
@jwt_required()
def comment_post(post_id):
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


@comment_api.route('/comments/for-post/<int:post_id>', methods=['GET'])
@jwt_required()
def post_comments(post_id):
    comments = Comment.query.filter(Comment.post_id == post_id)
    schema = CommentSchema(many=True)

    return jsonify(schema.dump(comments))