from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


API_KEY = "secret123"
HEADERS = {"Authorization": API_KEY}


def test_get_users_empty():
    response = client.get("/users/", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == []
