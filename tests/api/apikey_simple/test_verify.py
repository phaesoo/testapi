_VALID_TOKEN = "token-1"
_INVALID_TOKEN = "token-2"
_DUMMY_BODY = {"path": "/markets/all", "raw_query": ""}

_PATH = "/apikey-simple/verify"


def _generate_header(token: str):
    authorize_token = '{} {}'.format("Bearer", token)
    return {"Authorization": authorize_token}


def test_verify_returns_200(client):
    res = client.post(
        _PATH,
        headers=_generate_header(_VALID_TOKEN),
        json=_DUMMY_BODY,
    )
    assert res.status_code == 200


def test_verify_returns_401_with_invalid_token(client):
    res = client.post(
        _PATH,
        headers=_generate_header(_INVALID_TOKEN),
        json=_DUMMY_BODY,
    )
    assert res.status_code == 401


def test_verify_returns_401_with_unregistered_path_in_whitelists(client):
    body = _DUMMY_BODY.copy()
    body["path"] = "/markets/unregistered"
    res = client.post(
        _PATH,
        headers=_generate_header(_VALID_TOKEN),
        json=body,
    )
    assert res.status_code == 401
