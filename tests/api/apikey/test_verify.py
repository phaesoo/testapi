from uuid import uuid4

import jwt

_ACCESS_KEY = "123"
_SECRET_KEY = "456"
_DUMMY_BODY = {"path": "/markets/all", "raw_query": ""}


def _generate_header(payload: dict, prefix: str = "Bearer", secret_key: str = _SECRET_KEY):
    jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
    authorize_token = '{} {}'.format(prefix, jwt_token)
    return {"Authorization": authorize_token}


def test_verify_returns_200(client):
    payload = {"access_key": _ACCESS_KEY, "nonce": str(uuid4())}
    res = client.post(
        "/apikey/verify",
        headers=_generate_header(payload),
        json=_DUMMY_BODY,
    )
    assert res.status_code == 200


def test_verify_returns_401_without_nonce(client):
    payload = {"access_key": _ACCESS_KEY}
    res = client.post(
        "/apikey/verify",
        headers=_generate_header(payload),
        json=_DUMMY_BODY,
    )
    assert res.status_code == 401


def test_verify_returns_401_with_invalid_secret_key(client):
    payload = {"access_key": _ACCESS_KEY, "nonce": str(uuid4())}
    res = client.post(
        "/apikey/verify",
        headers=_generate_header(payload, secret_key="789"),
        json=_DUMMY_BODY,
    )
    assert res.status_code == 401


def test_verify_returns_401_with_invalid_token_prefix(client):
    payload = {"access_key": _ACCESS_KEY, "nonce": str(uuid4())}
    res = client.post(
        "/apikey/verify",
        headers=_generate_header(payload, prefix="Basic"),
        json=_DUMMY_BODY,
    )
    assert res.status_code == 401
