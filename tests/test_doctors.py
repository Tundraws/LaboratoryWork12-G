def test_unauthorized_doctors_access(client):
    response = client.get("/api/v1/doctors")
    assert response.status_code == 401
