from flask_jwt_extended import current_user

from api2 import db
from api2.models import Post



def test_add_comment(client, headers):
    post = Post(title="Boria2", type="Siqwell")
    db.session.add(post)
    db.session.commit()

    json_data = {"content": "I proud of you", "post_id": post.id}
    client.post('/api/comments', json=json_data, headers=headers)

    assert post.comments.first().id == post.id == 1


def test_delete_comment(client, headers):
    post = Post(title="Boria", type="Siqwell")
    db.session.add(post)
    db.session.commit()

    data = {"content": "I proud of you", "post_id": 1}
    rv = client.post('/api/comments', json=data, headers=headers)
    assert rv.status_code == 200

    sd = client.delete('/api/comments/1', headers=headers)
    sd.get_json()
    assert b"Comment with id - 1 was deleted." in sd.data

