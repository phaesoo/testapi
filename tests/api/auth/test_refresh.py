import pytest

_USERNAME = "test"
_PASSWORD = "testpw"


def _login(client):
    resp = client.post(
        "/auth/login",
        data={"username": _USERNAME, "password": _PASSWORD},
    )
    assert resp.status_code == 200

    return pytest.parse_body(resp)["access_token"]


def test_verify_returns_200(client):
    access_token = _login(client)
    resp = client.get(
        "/auth/refresh",
        headers={"Authorization": access_token}
    )
    assert resp.status_code == 200

    data = pytest.parse_body(resp)
    refreshed_token = data["access_token"]

    assert access_token != refreshed_token
