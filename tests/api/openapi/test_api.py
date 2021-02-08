def test_markets(client):
    resp = client.get("/markets/all")
    print(resp)
