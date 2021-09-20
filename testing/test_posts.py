from api2 import db
from api2.models import Post


def test_posts_list(client, headers):
    rv = client.get('/api/posts', headers=headers)
    assert rv.status_code == 200


def test_posts_create(client, headers):
    data = {
        "title": "Hobbit",
        "description": "Unexpected journey",
        "type": "Movie",
        "priority": 2
    }
    rv = client.post('/api/posts', json=data, headers=headers)
    assert rv.status_code == 201


def test_posts_one(client, headers):
    test_posts_create(client, headers)
    rv = client.get('/api/posts/1', headers=headers)
    assert rv.status_code == 200

    rv = client.get('/api/posts/2', headers=headers)
    assert rv.status_code == 404


def test_user_all_posts(client, user, headers):
    post = Post(title="Borov", priority=1, type='Movie', user_id=user.id)
    db.session.add(post)
    db.session.commit()

    rv = client.get('/api/users/1/posts', headers=headers)
    assert rv.status_code == 200
