from testing.test_registration import test_register


def test_login(client, user):
    test_register(client, user)
    data = {
        "username": user.username,
        "password": user.password
    }
    rv = client.post('/api/login', json=data)
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data.get('token')


def test_invalid_login_input_data(client):
    data = {"username": "cunarefa3", "password": "123"}
    rv = client.post('/api/auth/login', json=data)
    assert b"Couldn't verify!" in rv.data
    assert rv.status_code == 401
