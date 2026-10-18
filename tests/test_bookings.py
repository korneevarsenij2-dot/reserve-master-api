def  test_bookingsunauthorized(client):
    response = client.get("/bookings")
    assert response.status_code == 401
    