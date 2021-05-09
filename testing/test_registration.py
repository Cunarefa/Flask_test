def test_register(client):
    user_data = {"username": "nombre", "password": "12345", "email": "alfa@mail.ru"}
    rv = client.post('/api/register', json=user_data)
    assert {"token": rv.get_json('token')}


def test_invalid_register_input_data(client):
    user_data = {"username": "testuser2", "password": 12345, "email": "genryrich@mail.ru"}
    rv = client.post('/api/register', json=user_data)
    assert rv.status_code == 400


def test_lack_of_required_fields(client):
    data = {"username": "cunarefa", "password": "123"}
    rv = client.post('/api/register', json=data)
    assert rv.status_code == 400
