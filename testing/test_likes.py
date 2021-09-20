from api2 import db
from api2.models import Post
from api2.models.likes import likes


def test_like(client, user, headers):
    post = Post(title="Bobbit")
    db.session.add(post)
    db.session.commit()

    like = db.session.query(likes).filter(likes.c.user_id == user.id, likes.c.post_id == post.id).first()
    if not like:
        rv = client.post(f'/api/posts/{post.id}/likes', headers=headers)
        assert b"The post with Bobbit title was liked" in rv.data

    user.liked_posts.append(post)
    db.session.commit()
    rv = client.post(f'/api/posts/{post.id}/likes', headers=headers)
    assert b"You have already liked this post, Bitch" in rv.data


def test_unlike(client, headers, user):
    post = Post(title="Bobbit")
    db.session.add(post)
    db.session.commit()

    user.liked_posts.append(post)
    like = db.session.query(likes).filter(likes.c.user_id == user.id, likes.c.post_id == post.id).first()

    if like:
        rv = client.delete('/api/posts/1/likes', headers=headers)
        assert b"The post with 1 id was unliked" in rv.data

    rv = client.delete('/api/posts/1/likes', headers=headers)
    assert b"You didn't like this post" in rv.data
