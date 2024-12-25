# tests/test_transactions.py
from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_db

client = TestClient(app)

def test_get_transaction(db):
    response = client.get("/api/v1/transactions/0x123")
    assert response.status_code in [200, 404]

def test_get_address_transactions(db):
    response = client.get("/api/v1/address/0x123/transactions")
    assert response.status_code in [200, 404]