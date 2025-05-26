"""
Test suite for protected route access control.
This module contains tests for:
- Accessing protected routes with valid JWT tokens
- Access attempts without authentication
- Access attempts with invalid tokens
"""

from backend.app.models.user import User
from backend.app.core.security import hash_password, create_access_token
from datetime import datetime, timezone

def test_protected_route_with_valid_token(client, db_session):
    """
    Test accessing protected route with valid JWT token.
    
    Steps:
    1. Create a verified user
    2. Generate valid access token
    3. Make request with token in Authorization header
    
    Verifies:
    - Status code is 200 (OK)
    - Response contains welcome message
    - Message includes user's full name
    """
    # Create a verified user
    user = User(
        email="protected@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Protected User",
        is_verified=True,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Generate access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # Make request to protected route
    response = client.get(
        "/user/home",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome" in data["message"]
    assert "Protected User" in data["message"]

def test_protected_route_without_token(client):
    """
    Test accessing protected route without authentication token.
    
    Verifies:
    - Status code is 401 (Unauthorized)
    - Error message indicates not authenticated
    """
    response = client.get("/user/home")
    
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_protected_route_with_invalid_token(client):
    """
    Test accessing protected route with invalid JWT token.
    
    Verifies:
    - Status code is 401 (Unauthorized)
    - Error message indicates invalid credentials
    """
    response = client.get(
        "/user/home",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"] 