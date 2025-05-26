"""
Security module for handling password hashing, JWT token operations, and password validation.
This module provides functionality for secure password management and JWT-based authentication.
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from backend.app.config import get_settings
from typing import Optional
import re

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
    except jwt.JWTError:
        return None

class StrongPassword(str):
    """
    A custom string type that enforces strong password requirements.
    Implements Pydantic validation for password strength.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        
        def validate_password(value: str) -> str:
            """
            Validate password strength according to requirements.
            
            Args:
                value (str): The password to validate
                
            Returns:
                str: The validated password
                
            Raises:
                ValueError: If password doesn't meet strength requirements
            """
            if len(value) < 8:
                raise ValueError("Password must be at least 8 characters long")
            if not re.search(r"[A-Z]", value):
                raise ValueError("Password must contain at least one uppercase letter")
            if not re.search(r"[a-z]", value):
                raise ValueError("Password must contain at least one lowercase letter")
            if not re.search(r"\d", value):
                raise ValueError("Password must contain at least one number")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
                raise ValueError("Password must contain at least one special character")
            return value
        
        return core_schema.str_schema(
            min_length=8,
            custom_validator=validate_password
        )
