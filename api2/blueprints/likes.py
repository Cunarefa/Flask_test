from flask_jwt_extended import jwt_required, current_user

from api2 import db
from api2.blueprints import like_api
from api2.models import Post
from api2.models.likes import likes


@like_api.route('/like/post/<int:post_id>', methods=['GET'])
@jwt_required()
def like_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    liked_posts = Post.query.filter(likes.c.post_id == post.id).first()
    if not liked_posts:
        current_user.liked_posts.append(post)
        db.session.commit()
        return {"message": f"The post with {post_id} id was liked"}
    return {"message": "You have already liked this post, Bitch"}


@like_api.route('/unlike/post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    current_user.liked_posts.remove(post)
    db.session.commit()
    return {"message": f"The post with {post_id} id was unliked"}
