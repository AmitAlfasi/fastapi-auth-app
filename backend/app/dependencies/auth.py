"""
Authentication dependencies module for FastAPI.
This module provides dependency functions for handling JWT token authentication and user verification.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.database import get_db
from backend.app.core.security import verify_token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from the JWT token.
    
    Args:
        token (str): JWT token from the Authorization header
        db (Session): Database session dependency
        
    Returns:
        User: The authenticated user object
        
    Raises:
        HTTPException: If the token is invalid or the user is not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    # Use verify_token instead of direct jwt.decode
    payload = verify_token(token)
    if not payload:
        raise credentials_exception

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user
