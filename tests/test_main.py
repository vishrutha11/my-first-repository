# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from main import app, fake_db, User

client = TestClient(app)

# Reset fake_db before each test
@pytest.fixture(autouse=True)
def clear_db():
    fake_db.clear()
    yield


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "age" in data
    assert "gender" in data


def test_create_user():
    user_data = {"id": 1, "name": "Alice", "email": "alice@example.com"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert len(fake_db) == 1  # Confirm user was added


def test_get_user_found():
    # Add a user manually
    user = User(id=2, name="Bob", email="bob@example.com")
    fake_db.append(user)

    response = client.get("/users/2")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["name"] == "Bob"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_found():
    user = User(id=3, name="Charlie", email="charlie@example.com")
    fake_db.append(user)

    response = client.delete("/users/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert len(fake_db) == 0  # Confirm user was deleted


def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
