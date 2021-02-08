def test_markets(client):
    resp = client.get("/markets/all")
    assert resp.status_code == 200
