from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["semantic_mode"] in {"rule-based-fallback", "sentence-transformers"}
    assert "X-Process-Time-Ms" in response.headers


def test_taxonomy_endpoint_lists_skills():
    response = client.get("/api/taxonomy")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_skills"] >= 43
    assert "Programming" in payload["categories"]


def test_analyze_endpoint_returns_explanations():
    response = client.post("/api/analyze", json={
        "resume_text": "Built apps with Python, React, and Docker.",
        "job_description": "Required: Python and SQL. Preferred: React.",
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["requirements_found"] == 3
    assert payload["strong_matches"] == 2
    assert payload["missing_skills"] == 1
    assert payload["methodology_note"]
    assert payload["score_band"]
    assert "Docker" in payload["extra_resume_skills"]
    assert len(payload["category_breakdown"]) >= 2


def test_analyze_endpoint_rejects_job_without_supported_skills():
    response = client.post("/api/analyze", json={
        "resume_text": "A general student profile.",
        "job_description": "We are looking for a motivated team player.",
    })
    assert response.status_code == 422


def test_compare_endpoint_ranks_jobs():
    response = client.post("/api/compare", json={
        "resume_text": "Built REST APIs with Python, FastAPI, PostgreSQL, and Docker.",
        "jobs": [
            {"title": "Frontend Intern", "job_description": "Required: React, TypeScript, CSS."},
            {"title": "Backend Intern", "job_description": "Required: Python, FastAPI, PostgreSQL, Docker."},
        ],
    })
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["rankings"]) == 2
    assert payload["rankings"][0]["title"] == "Backend Intern"
    assert payload["rankings"][0]["overall_score"] > payload["rankings"][1]["overall_score"]


def test_resume_parse_supports_txt_and_rejects_unsupported():
    txt_resp = client.post(
        "/api/resume/parse",
        files={"file": ("resume.txt", b"Built APIs with Python and FastAPI.", "text/plain")},
    )
    assert txt_resp.status_code == 200
    assert "FastAPI" in txt_resp.json()["text"]

    bad_resp = client.post(
        "/api/resume/parse",
        files={"file": ("resume.exe", b"binary", "application/octet-stream")},
    )
    assert bad_resp.status_code == 400
