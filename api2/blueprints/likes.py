from flask_jwt_extended import jwt_required, current_user

from api2 import db
from api2.blueprints import like_api
from api2.models import Post


@like_api.route('/like/<int:post_id>', methods=['GET'])
@jwt_required()
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    current_user.like_post(post)
    db.session.commit()
    return {"message": f"The post with {post_id} id was liked"}


@like_api.route('/unlike/<int:post_id>', methods=['GET'])
@jwt_required()
def unlike_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    current_user.unlike_post(post)
    db.session.commit()
    return {"message": f"The post with {post_id} id was unliked"}
