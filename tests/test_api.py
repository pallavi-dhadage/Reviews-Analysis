from fastapi.testclient import TestClient
from src.api.main import app
from src.config import settings

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_analyze_endpoint():
    payload = {"text": "I really love this product!"}
    response = client.post(f"{settings.API_V1_STR}/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == payload["text"]
    assert "sentiment_score" in data
    assert "sentiment_label" in data
    assert data["sentiment_label"] in ["positive", "negative", "neutral"]
