import pytest
from fastapi.testclient import TestClient
from app.routes.user import get_all_users,get_user_by_id
from .mock_db import mock_user_db
from app.main import app
from app.models import User

client = TestClient(app)

#converted json response to pydantic class to compare except metadata
def test_get_all_user(mock_user_db):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    for user_id,user_data in data.items():
        response_user = User(**user_data)
        response_fields = response_user.model_dump(exclude={'created_at' , 'updated_at'})
        original_user = mock_user_db[int(user_id)]
        original_fields = original_user.model_dump(exclude={'created_at' , 'updated_at'})

        assert response_fields == original_fields
        

def test_get_user_by_correct_id(mock_user_db):
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

def test_get_user_by_wrong_id(mock_user_db):
    user_id = 123
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_create_user(mock_user_db):
    new_user = {
    "user_id": 0,
    "name": "new test user",
    "email": "user@example.com",
    "phone_no": 0,
    "salary": 1,
        }
    response = client.post("/users",json = new_user) 
    assert response.status_code == 201
   
def test_delete_user(mock_user_db):
    user_id = 1
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
