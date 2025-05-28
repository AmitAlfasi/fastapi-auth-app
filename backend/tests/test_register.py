"""
Test suite for user registration functionality.
This module contains tests for:
- Successful user registration
- Registration with existing email
- Password validation and matching
- Password strength requirements
"""

import pytest
from backend.app.models.user import User
from backend.app.core.security import hash_password
from datetime import datetime, timezone

def test_register_success(client):
    """
    Test successful user registration with valid data.
    
    Verifies:
    - Status code is 201 (Created)
    - Response contains user_id
    - Success message is returned
    """
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test123!@#",
            "confirm_password": "Test123!@#",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code == 201
    assert "user_id" in response.json()
    assert "message" in response.json()
    assert "registered successfully" in response.json()["message"]

def test_register_existing_email(client, db_session):
    """
    Test registration attempt with an email that's already registered.
    
    Steps:
    1. Create a user with test email
    2. Attempt to register another user with same email
    
    Verifies:
    - Status code is 400 (Bad Request)
    - Error message indicates email is already registered
    """
    # Create a user first
    existing_user = User(
        email="test@example.com",
        hashed_password=hash_password("Test123!@#"),
        full_name="Test User",
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(existing_user)
    db_session.commit()
    
    # Try to register with same email
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test123!@#",
            "confirm_password": "Test123!@#",
            "full_name": "Another User"
        }
    )
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_register_password_mismatch(client):
    """
    Test registration with non-matching password and confirmation.
    
    Verifies:
    - Status code is 422 (Unprocessable Entity)
    - Error message indicates passwords don't match
    """
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test123!@#",
            "confirm_password": "Different123!@#",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code == 422
    assert "Passwords do not match" in response.json()["detail"][0]["msg"]

@pytest.mark.parametrize("password, expected_error", [
    ("test123!@#", "uppercase letter"),
    ("TEST123!@#", "lowercase letter"),
    ("Test!@#$", "number"),
    ("Test", "8"),
    (123, "string")

])
def test_register_weak_password(client, password, expected_error):
    """
    Test registration with passwords that don't meet strength requirements.
    
    Args:
        password (str): Password to test
        expected_error (str): Expected error message fragment
        
    Verifies:
    - Status code is 422 (Unprocessable Entity)
    - Error message indicates specific password requirement not met
    """
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": password,
            "confirm_password": password,
            "full_name": "Test User"
        }
    )

    assert response.status_code == 422
    assert expected_error in response.json()["detail"][0]["msg"] 