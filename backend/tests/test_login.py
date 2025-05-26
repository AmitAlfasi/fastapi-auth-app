"""
Test suite for user login functionality.
This module contains tests for:
- Successful login with valid credentials
- Login attempts with invalid credentials
- Login attempts with unverified users
- Error handling for various login scenarios
"""

from backend.app.models.user import User
from backend.app.core.security import hash_password
from datetime import datetime, timezone

def test_login_success(client, db_session):
    """
    Test successful login with valid credentials.
    
    Steps:
    1. Create a verified user in the database
    2. Attempt login with correct credentials
    
    Verifies:
    - Status code is 200 (OK)
    - Response contains valid access token
    - Token type is 'bearer'
    """
    # Create a verified user
    user = User(
        email="user@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Login Test",
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Attempt login
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "ValidPass123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, db_session):
    """
    Test login attempt with incorrect password.
    
    Steps:
    1. Create a verified user in the database
    2. Attempt login with wrong password
    
    Verifies:
    - Status code is 401 (Unauthorized)
    - Error message indicates invalid credentials
    """
    # Create a verified user
    user = User(
        email="user@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Login Test",
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Attempt login with wrong password
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "WrongPass456"
        }
    )
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_login_nonexistent_email(client):
    """
    Test login attempt with non-existent email.
    
    Verifies:
    - Status code is 401 (Unauthorized)
    - Error message indicates invalid credentials
    """
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "AnyPass123"
        }
    )
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_login_unverified_user(client, db_session):
    """
    Test login attempt with unverified user account.
    
    Steps:
    1. Create an unverified user in the database
    2. Attempt login with correct credentials
    
    Verifies:
    - Status code is 403 (Forbidden)
    - Error message indicates email not verified
    """
    # Create an unverified user
    user = User(
        email="unverified@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Unverified User",
        is_verified=False,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Attempt login
    response = client.post(
        "/auth/login",
        json={
            "email": "unverified@example.com",
            "password": "ValidPass123"
        }
    )
    
    assert response.status_code == 403
    assert "Email not verified" in response.json()["detail"] 