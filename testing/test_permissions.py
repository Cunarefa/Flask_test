from flask_jwt_extended import create_access_token

from api2 import db
from api2.models import Post, User


def test_add_comment_with_viewer_role(client):
    user = User(username="testuser1", password="12345", email="aldo@msail.ru",
                role="VIEWER", )
    post = Post(title="Boria2", type="Siqwell")
    db.session.add(post)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.username)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    json_data = {"content": "I proud of you", "post_id": post.id}
    rv = client.post('/api/comments', json=json_data, headers=headers)

    assert rv.status_code == 403


def test_add_comment_with_editor_role(client):
    user = User(username="testuser1", password="12345", email="aldo@msail.ru",
                role="EDITOR", )
    post = Post(title="Boria", type="Siqwell")
    db.session.add(user)
    db.session.add(post)
    db.session.commit()

    access_token = create_access_token(identity=user.username)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    json_data = {"content": "I proud of you", "post_id": post.id}
    rv = client.post('/api/comments', json=json_data, headers=headers)

    assert rv.status_code == 200
    assert post.comments.first().id == post.id == 1
