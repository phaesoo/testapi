import pytest

_USERNAME = "test"
_PASSWORD = "testpw"


def _login(client):
    resp = client.post(
        "/auth/login",
        data={"username": _USERNAME, "password": _PASSWORD},
    )
    assert resp.status_code == 200

    return pytest.parse_body(resp)["access_key"]


def test_verify_returns_200(client):
    access_key = _login(client)
    resp = client.get(
        "/auth/verify",
        headers={"Authorization": access_key}
    )
    assert resp.status_code == 200
