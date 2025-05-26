"""
Test suite for refresh token functionality.
This module contains tests for:
- Successful token refresh with valid refresh token
- Refresh attempts with invalid tokens
- Refresh attempts with expired tokens
"""

from backend.app.models.user import User
from backend.app.models.refresh_token import RefreshToken
from backend.app.core.security import hash_password, create_refresh_token
from backend.app.config import get_settings
from datetime import datetime, timezone
from hashlib import sha256

def test_refresh_token_success(client, db_session):
    """
    Test successful access token refresh with valid refresh token.
    
    Steps:
    1. Create a verified user
    2. Generate and store refresh token
    3. Set refresh token in client cookies
    4. Attempt token refresh
    
    Verifies:
    - Status code is 200 (OK)
    - New access token is returned
    - Access token is valid format
    """
    # Create a verified user
    user = User(
        email="refresh@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Refresh User",
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Create a refresh token
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    hashed_token = sha256(refresh_token.encode()).hexdigest()
    
    # Store the refresh token
    db_token = RefreshToken(
        token=hashed_token,
        user_id=user.id
    )
    db_session.add(db_token)
    db_session.commit()
    
    # Set cookie on client
    client.cookies.set("refresh_token", refresh_token)
    
    # Attempt refresh
    response = client.post("/auth/refresh")
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0

def test_refresh_token_invalid(client):
    """
    Test refresh attempt with invalid refresh token.
    
    Steps:
    1. Set invalid refresh token in client cookies
    2. Attempt token refresh
    
    Verifies:
    - Status code is 401 (Unauthorized)
    - Error message indicates invalid token
    """
    # Set invalid cookie on client
    client.cookies.set("refresh_token", "invalid.token.here")
    
    response = client.post("/auth/refresh")
    
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]

def test_refresh_token_expired(client, db_session):
    """
    Test refresh attempt with expired refresh token.
    
    Steps:
    1. Create a verified user
    2. Generate and store expired refresh token
    3. Set expired token in client cookies
    4. Attempt token refresh
    
    Verifies:
    - Status code is 401 (Unauthorized)
    - Error message indicates invalid token
    """
    # Create a verified user
    user = User(
        email="refresh@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Refresh User",
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Create an expired refresh token
    settings = get_settings()
    settings.REFRESH_TOKEN_EXPIRE_DAYS = -1  # Force expiration
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    hashed_token = sha256(refresh_token.encode()).hexdigest()
    
    # Store the refresh token
    db_token = RefreshToken(
        token=hashed_token,
        user_id=user.id
    )
    db_session.add(db_token)
    db_session.commit()
    
    # Set expired cookie on client
    client.cookies.set("refresh_token", refresh_token)
    
    # Attempt refresh
    response = client.post("/auth/refresh")
    
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"] 