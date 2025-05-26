"""
Test suite for user logout functionality.
This module contains tests for:
- Successful logout with refresh token
- Logout behavior without refresh token
- Cookie and database cleanup after logout
"""

from backend.app.models.user import User
from backend.app.models.refresh_token import RefreshToken
from backend.app.core.security import hash_password, create_refresh_token
from datetime import datetime, timezone
from hashlib import sha256

def test_logout_clears_cookie(client, db_session):
    """
    Test that logout properly clears refresh token cookie and database entry.
    
    Steps:
    1. Create a verified user
    2. Generate and store refresh token
    3. Set refresh token in client cookies
    4. Perform logout
    
    Verifies:
    - Status code is 204 (No Content)
    - Refresh token cookie is cleared
    - Refresh token is removed from database
    """
    # Create a verified user
    user = User(
        email="logout@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Logout Test User",
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
    
    # Attempt logout
    response = client.post("/auth/logout")
    
    # Check response
    assert response.status_code == 204
    
    # Verify cookie is cleared
    assert "refresh_token" not in response.cookies
    
    # Verify token is removed from database
    db_token = db_session.query(RefreshToken).filter_by(token=hashed_token).first()
    assert db_token is None

def test_logout_with_no_cookie(client):
    """
    Test logout behavior when no refresh token cookie is present.
    
    Verifies:
    - Status code is 204 (No Content)
    - No error is raised
    - No refresh token cookie is set
    """
    # Attempt logout without setting any cookie
    response = client.post("/auth/logout")
    
    # Check response - should still succeed
    assert response.status_code == 204
    
    # Verify no error is raised
    assert "refresh_token" not in response.cookies 