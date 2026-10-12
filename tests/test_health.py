from fastapi.testclient import TestClient

from backend_challenge_python.main import app


def test_health():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
