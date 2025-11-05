# tests/test_api.py
from fastapi.testclient import TestClient
import app as app_module

client = TestClient(app_module.app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict_minimal():
    r = client.post("/predict", json={"text": "My invoice is wrong"})
    assert r.status_code == 200
    body = r.json()
    assert "label" in body and "confidence" in body and "suggested_response" in body
