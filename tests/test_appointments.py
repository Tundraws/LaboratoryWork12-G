def test_unauthorized_appointments_access(client):
    response = client.get("/api/v1/appointments")
    assert response.status_code == 401
