import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Bill
from .mock_db import mock_bill_db

client = TestClient(app)

# 1. GET ALL BILLS FOR A USER
def test_get_user_bills_success(mock_bill_db):
    user_id = 1
    response = client.get(f"/users/{user_id}/bills")
    assert response.status_code == 200
    # Check if the returned bills actually belong to user 1
    for bill_id, bill_data in response.json().items():
        assert bill_data["user_id"] == user_id

def test_get_user_bills_user_not_found(mock_bill_db):
    response = client.get("/users/999/bills")
    assert response.status_code == 404

# 2. GET SINGLE BILL BY ID
def test_get_bill_by_id_success(mock_bill_db):
    user_id = 1
    bill_id = 1
    response = client.get(f"/users/{user_id}/bills/{bill_id}")
    assert response.status_code == 200
    assert response.json()["bill_id"] == bill_id

def test_get_bill_by_id_not_found(mock_bill_db):
    user_id = 1
    bill_id = 4
    response = client.get(f"/users/{user_id}/bills/{bill_id}")
    assert response.status_code == 404

def test_get_bill_forbidden(mock_bill_db):
    # Trying to access User 2's bill using User 1's path
    user_id = 1
    bill_id = 2 # Assume Bill 2 belongs to User 2 in your mock_db
    response = client.get(f"/users/{user_id}/bills/{bill_id}")
    assert response.status_code == 403

# 3. CREATE BILL
def test_create_bill_success(mock_bill_db):
    user_id = 1
    new_bill = {
        "bill_id": 10,
        "user_id": 1,
        "type": "Electricity",
        "description": "Feb Payment",
        "is_paid": False,
        "cost": 500.0,
        "due_date": "2026-03-01"
    }
    response = client.post(f"/users/{user_id}/bills", json=new_bill)
    assert response.status_code == 201
    assert response.json()["type"] == "Electricity"

# 4. UPDATE BILL (PATCH)
def test_update_bill_success(mock_bill_db):
    user_id = 1
    bill_id = 1
    update_data = {"is_paid": True, "cost": 1200.0}
    response = client.patch(f"/users/{user_id}/bills/{bill_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["is_paid"] is True
    assert response.json()["cost"] == 1200.0

def test_update_bill_forbidden(mock_bill_db):
    user_id = 2
    bill_id = 1
    update_data = {"is_paid": True, "cost": 1200.0}
    response = client.patch(f"/users/{user_id}/bills/{bill_id}", json=update_data)
    assert response.status_code == 403

# 5. DELETE BILL
def test_delete_bill_success(mock_bill_db):
    user_id = 1
    bill_id = 1
    response = client.delete(f"/users/{user_id}/bills/{bill_id}")
    assert response.status_code == 204

def test_delete_bill_forbidden(mock_bill_db):
    user_id = 1
    bill_id = 2
    response = client.delete(f"/users/{user_id}/bills/{bill_id}")
    assert response.status_code == 403