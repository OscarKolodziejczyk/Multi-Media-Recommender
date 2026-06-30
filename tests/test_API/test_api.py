from fastapi.testclient import TestClient
from src.API.main import app

client = TestClient(app)

def test_read_root():
    """
    Server health check
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Status": "Multi Media Recommendation Engine Live"}

def test_valid_recommendation():
    """
    Test golden response: search for a known title, and confirm correct response
    """
    response = client.get("/recommend/The Matrix")

    assert response.status_code == 200

    data = response.json()

    assert data["searched_title"] == "The Matrix"
    assert "recommendations" in data
    assert len(data["recommendations"]) == 15

def test_invalid_recommendation():
    """
    Test an invalid movie title
    """
    response = client.get("/recommend/InvalidMovie")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Title InvalidMovie not found'}
