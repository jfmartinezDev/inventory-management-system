"""
Test cases for authentication endpoints.
Tests login, registration, and token generation.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings


def test_register_user(client: TestClient, db: Session):
    """Test user registration."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "full_name": "New User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data


def test_register_duplicate_username(client: TestClient, db: Session, test_user):
    """Test registration with duplicate username."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "username": test_user["username"],
            "email": "another@example.com",
            "password": "password123",
            "full_name": "Another User"
        }
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_register_duplicate_email(client: TestClient, db: Session, test_user):
    """Test registration with duplicate email."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "username": "anotheruser",
            "email": test_user["email"],
            "password": "password123",
            "full_name": "Another User"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client: TestClient, db: Session, test_user):
    """Test successful login."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_email(client: TestClient, db: Session, test_user):
    """Test login with email instead of username."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client: TestClient, db: Session, test_user):
    """Test login with wrong password."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_user["username"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient, db: Session):
    """Test login with non-existent user."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "nonexistent",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

