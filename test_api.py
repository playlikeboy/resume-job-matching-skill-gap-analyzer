from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_endpoint_returns_explanations():
    response = client.post("/api/analyze", json={
        "resume_text": "Built apps with Python and React.",
        "job_description": "Required: Python and SQL. Preferred: React.",
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["requirements_found"] == 3
    assert payload["strong_matches"] == 2
    assert payload["missing_skills"] == 1
    assert payload["methodology_note"]


def test_analyze_endpoint_rejects_job_without_supported_skills():
    response = client.post("/api/analyze", json={
        "resume_text": "A general student profile.",
        "job_description": "We are looking for a motivated team player.",
    })
    assert response.status_code == 422
