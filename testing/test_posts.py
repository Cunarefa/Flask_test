from flask_jwt_extended import create_access_token


def test_posts_list(client, user, user_register):
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    rv = client.get('/api/posts', headers=headers)
    assert rv.status_code == 200


def test_posts_without_token(client):
    rv = client.get('/api/posts')
    assert rv.status_code == 401


def test_posts_create(client, user, user_register):
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    data = {
        "title": "Hobbit",
        "description": "Unexpected journey",
        "type": "Movie",
        "priority": 1
    }
    rv = client.post('/api/posts/create', json=data, headers=headers)
    assert rv.status_code == 201


def test_posts_one(client, user, user_register):
    test_posts_create(client, user, user_register)
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    rv = client.get('/api/posts/get/1', headers=headers)
    assert rv.status_code == 200


def test_posts_none(client, user, user_register):
    test_posts_create(client, user, user_register)
    access_token = create_access_token(identity=user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    rv = client.get('/api/posts/2/get', headers=headers)
    assert rv.status_code == 404
