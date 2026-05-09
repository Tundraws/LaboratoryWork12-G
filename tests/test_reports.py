def test_unauthorized_reports_access(client):
    response = client.get("/api/v1/reports/doctors/by-patients-count")
    assert response.status_code == 401
