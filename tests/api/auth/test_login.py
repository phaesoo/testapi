def test_login_returns_200(client):
    resp = client.post(
        "/auth/login",
        data={"username": "test", "password": "testpw"},
    )
    assert resp.status_code == 200


def test_login_returns_422_without_required_param(client):
    resp = client.post("/auth/login")
    assert resp.status_code == 422


def test_login_returns_400_with_invalid_username(client):
    resp = client.post(
        "/auth/login",
        data={"username": "test2", "password": "testpw"},
    )
    assert resp.status_code == 400


def test_login_returns_400_with_invalid_password(client):
    resp = client.post(
        "/auth/login",
        data={"username": "test", "password": "testpw1"},
    )
    assert resp.status_code == 400
