from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_health_api():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_demo_jobs_api():
    response = client.get("/api/demo/jobs")
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 2

def test_adventure_start_api():
    response = client.post("/api/adventure/start", json={"job_id": "demo-data-engineer"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "hero_story" in response.json()["data"]

def test_interview_challenge_api():
    response = client.post("/api/interview/challenge", json={"job_id": "demo-data-engineer"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "monster" in response.json()["data"]
