from app.models.user import User
from app.core.security import hash_password, create_access_token
from datetime import datetime, timezone

def test_protected_route_with_valid_token(client, db_session):
    """Test accessing protected route with valid token"""
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
    """Test accessing protected route without token"""
    response = client.get("/user/home")
    
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_protected_route_with_invalid_token(client):
    """Test accessing protected route with invalid token"""
    response = client.get(
        "/user/home",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"] 