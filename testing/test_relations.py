from api2 import db
from api2.models import Post


def test_like(client, user):
    post = Post(title="Boria", type="Siqwell")
    post2 = Post(title="Gatsby", type="Treesome")
    db.session.add(user)
    db.session.add(post)
    db.session.add(post2)
    db.session.commit()

    user.like_post(post)
    db.session.commit()
    assert user.has_liked(post)
    assert user.has_liked(post2) is False


def test_unlike(client, user):
    post = Post(title="Boria2", type="Siqwell")
    post2 = Post(title="GatsbyBoy", type="Treesome")
    db.session.add(user)
    db.session.add(post)
    db.session.add(post2)
    db.session.commit()

    user.like_post(post2)
    db.session.commit()
    user.unlike_post(post2)
    assert user.has_liked(post) is False
    assert user.has_liked(post2) is False


def test_comments(client, user):
    post = Post(title="Boria2", type="Siqwell")
    db.session.add(user)
    db.session.add(post)
    db.session.commit()

    data = {"content": "I proud of you"}
    content = data['content']
    user.comment_post(post, content)
    post.post_comments
    assert user.has_commented(post)
    assert post.comments.count() == 1
