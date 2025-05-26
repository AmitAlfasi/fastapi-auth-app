from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import hash_password, create_refresh_token
from datetime import datetime, timezone
from hashlib import sha256

def test_logout_clears_cookie(client, db_session):
    """Test that logout clears the refresh token cookie"""
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
    """Test that logout works even without a cookie"""
    # Attempt logout without setting any cookie
    response = client.post("/auth/logout")
    
    # Check response - should still succeed
    assert response.status_code == 204
    
    # Verify no error is raised
    assert "refresh_token" not in response.cookies 