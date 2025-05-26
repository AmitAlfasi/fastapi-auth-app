"""
Test suite for email verification functionality.
This module contains tests for:
- Successful email verification with valid code
- Verification attempts with invalid codes
- Verification attempts with expired codes
- User verification status updates
"""

from backend.app.models.user import User
from backend.app.models.verification_code import VerificationCode
from backend.app.core.security import hash_password
from datetime import datetime, timezone, timedelta

def test_email_verification_success(client, db_session):
    """
    Test successful email verification with valid code.
    
    Steps:
    1. Create an unverified user
    2. Create a valid verification code
    3. Submit verification request
    
    Verifies:
    - Status code is 200 (OK)
    - Success message is returned
    - User is marked as verified in database
    """
    # Create an unverified user
    user = User(
        email="verify@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Verify User",
        is_verified=False,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Create a valid verification code
    verification_code = VerificationCode(
        user_id=user.id,
        code="123456",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        is_used=False
    )
    db_session.add(verification_code)
    db_session.commit()
    
    # Attempt verification
    response = client.post(
        "/auth/verify-email",
        json={
            "email": "verify@example.com",
            "code": "123456"
        }
    )
    
    assert response.status_code == 200
    assert "Email verified successfully" in response.json()["message"]
    
    # Verify user is marked as verified
    db_session.refresh(user)
    assert user.is_verified == True

def test_email_verification_invalid_code(client, db_session):
    """
    Test email verification with incorrect code.
    
    Steps:
    1. Create an unverified user
    2. Create a valid verification code
    3. Submit verification with wrong code
    
    Verifies:
    - Status code is 400 (Bad Request)
    - Error message indicates invalid code
    - User remains unverified
    """
    # Create an unverified user
    user = User(
        email="verify@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Verify User",
        is_verified=False,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Create a valid verification code
    verification_code = VerificationCode(
        user_id=user.id,
        code="123456",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        is_used=False
    )
    db_session.add(verification_code)
    db_session.commit()
    
    # Attempt verification with wrong code
    response = client.post(
        "/auth/verify-email",
        json={
            "email": "verify@example.com",
            "code": "999999"
        }
    )
    
    assert response.status_code == 400
    assert "Invalid or expired verification code" in response.json()["detail"]
    
    # Verify user is still unverified
    db_session.refresh(user)
    assert user.is_verified == False

def test_email_verification_expired_code(client, db_session):
    """
    Test email verification with expired code.
    
    Steps:
    1. Create an unverified user
    2. Create an expired verification code
    3. Submit verification request
    
    Verifies:
    - Status code is 400 (Bad Request)
    - Error message indicates invalid/expired code
    - User remains unverified
    """
    # Create an unverified user
    user = User(
        email="verify@example.com",
        hashed_password=hash_password("ValidPass123"),
        full_name="Verify User",
        is_verified=False,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    
    # Create an expired verification code
    verification_code = VerificationCode(
        user_id=user.id,
        code="123456",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=30),
        is_used=False
    )
    db_session.add(verification_code)
    db_session.commit()
    
    # Attempt verification with expired code
    response = client.post(
        "/auth/verify-email",
        json={
            "email": "verify@example.com",
            "code": "123456"
        }
    )
    
    assert response.status_code == 400
    assert "Invalid or expired verification code" in response.json()["detail"]
    
    # Verify user is still unverified
    db_session.refresh(user)
    assert user.is_verified == False 