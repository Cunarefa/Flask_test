from flask_jwt_extended import jwt_required, current_user

from api2 import db
from api2.blueprints import like_api
from api2.models import Post
from api2.perm_decorators import roles_required


@like_api.route('/post/<int:post_id>/likes', methods=['GET'])
@jwt_required()
@roles_required('Editor')
def like_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    liked_posts = current_user.liked_posts.all()
    if post not in liked_posts:
        current_user.liked_posts.append(post)
        db.session.commit()
        return {"message": f"The post with {post_id} id was liked"}
    return {"message": "You have already liked this post, Bitch"}


@like_api.route('/post/<int:post_id>/likes', methods=['DELETE'])
@jwt_required()
@roles_required('Editor')
def unlike_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    current_user.liked_posts.all().remove(post)
    db.session.commit()
    return {"message": f"The post with {post_id} id was unliked"}
