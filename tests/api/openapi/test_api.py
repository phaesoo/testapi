def test_markets(client):
    resp = client.get("/api/market/all")
    print(resp)
