def test_admin_role(client, headers):
    rv = client.get('/api/posts/testing', headers=headers)
    # data = rv.get_json()
    assert rv.status_code == 403