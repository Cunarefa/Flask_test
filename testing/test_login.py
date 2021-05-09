from testing.test_registration import test_register


def test_login(client):
    test_register(client)
    data = {
        "username": "nombre",
        "password": "12345"
    }
    rv = client.post('/api/login', json=data)
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data.get('token')


def test_invalid_login_input_data(client):
    data = {"username": "cunarefa3", "password": "123"}
    rv = client.post('/api/login', json=data)
    assert b"Couldn't verify!" in rv.data
    assert rv.status_code == 401
