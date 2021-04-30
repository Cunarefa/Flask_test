from api2 import db
from api2.models import Post


def test_add_comment(client, user, user_register, headers):
    post = Post(title="Boria2", type="Siqwell")
    db.session.add(post)
    db.session.commit()

    data = {"content": "I proud of you"}
    rv = client.post('/api/comments/add/onPost/1', json=data, headers=headers)
    assert rv.status_code == 200


def test_delete_comment(client, user, user_register, headers):
    post = Post(title="Boria", type="Siqwell")
    db.session.add(post)
    db.session.commit()

    data = {"content": "I proud of you"}
    client.post('/api/comments/add/onPost/1', json=data, headers=headers)

    sd = client.delete('/api/comments/delete/1/comment/fromPost/1', headers=headers)
    assert sd.status_code == 200


# def test_update_comment(client, headers):
#     post = Post(title="Boria2", type="Siqwell")
#     db.session.add(post)
#     db.session.commit()
#
#     new_data = {"content": "New data"}
#
#     rv = client.patch('/api/comments/update/1', json=new_data, headers=headers)
#     assert rv.status_code == 200
