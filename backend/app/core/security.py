from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import get_settings
from typing import Optional
import re

# Use bcrypt for secure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    settings = get_settings()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, get_settings().JWT_SECRET, algorithms=[get_settings().ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

class StrongPassword(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        
        def validate_password(value: str) -> str:
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
