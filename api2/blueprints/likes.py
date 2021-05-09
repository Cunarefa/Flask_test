from flask_jwt_extended import jwt_required, current_user

from api2 import db
from api2.blueprints import like_api
from api2.models import Post
from api2.models.enums import Role
from api2.models.likes import likes
from api2.perm_decorators import roles_required


@like_api.route('/posts/<int:post_id>/likes', methods=['POST'])
@jwt_required()
@roles_required(Role.EDITOR)
def like_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    like = db.session.query(likes).filter(likes.c.user_id == current_user.id, likes.c.post_id == post.id).first()
    if not like:
        current_user.liked_posts.append(post)
        db.session.commit()
        return {"message": f"The post with {post.title} title was liked"}
    return {"message": "You have already liked this post, Bitch"}


@like_api.route('/posts/<int:post_id>/likes', methods=['DELETE'])
@jwt_required()
@roles_required(Role.EDITOR)
def unlike_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    like = db.session.query(likes).filter(likes.c.user_id == current_user.id, likes.c.post_id == post.id).first()
    if like:
        current_user.liked_posts.remove(post)
        db.session.commit()
        return {"message": f"The post with {post_id} id was unliked"}
    return {"message": "You didn't like this post"}
