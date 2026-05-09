def test_unauthorized_patients_access(client):
    response = client.get("/api/v1/patients")
    assert response.status_code == 401
