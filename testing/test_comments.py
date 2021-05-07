from api2 import db
from api2.models import Post


def test_add_comment(client, headers):
    post = Post(title="Boria2", type="Siqwell")
    db.session.add(post)
    db.session.commit()

    json_data = {"content": "I proud of you", "post_id": 1}
    rv = client.post('/api/posts/1/comments', json=json_data, headers=headers)
    data = rv.get_json()
    assert data['post_id'] == 1


def test_delete_comment(client, headers):
    post = Post(title="Boria", type="Siqwell")
    db.session.add(post)
    db.session.commit()

    data = {"content": "I proud of you", "post_id": 1}
    rv = client.post('/api/posts/1/comments', json=data, headers=headers)
    assert rv.status_code == 200

    sd = client.delete('/api/comments/1', headers=headers)
    sd.get_json()
    assert b"Comment with 1 id was deleted." in sd.data

