"""
Security module for handling password hashing and JWT token operations.
This module provides functionality for secure password management and JWT-based authentication.
"""
from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from backend.app.config import get_settings
from typing import Optional

# Use bcrypt for secure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password to compare against
        
    Returns:
        bool: True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data (dict): The data to encode in the token
        expires_delta (Optional[timedelta]): Custom expiration time. If None, uses default from settings
        
    Returns:
        str: The encoded JWT token
    """
    
    settings = get_settings()

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token with longer expiration.
    
    Args:
        data (dict): The data to encode in the token
        
    Returns:
        str: The encoded JWT refresh token
    """
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.
    
    Args:
        token (str): The JWT token to verify
        
    Returns:
        Optional[dict]: The decoded token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, get_settings().JWT_SECRET, algorithms=[get_settings().ALGORITHM])
        return payload
    except ExpiredSignatureError:
        print("Token expired")
        return None
    except JWTError:
        print("Invalid token")
        return None

