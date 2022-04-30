from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_graph():
    response = client.get("/graph")
    assert response.status_code == 200


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text.__contains__("Book API")
