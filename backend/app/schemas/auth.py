"""
Authentication schema module defining Pydantic models for authentication-related requests.
This module provides data validation and serialization for login, email verification, and related operations.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class ResendVerificationCodeRequest(BaseModel):
    """
    Request model for resending verification code.
    
    Attributes:
        email (EmailStr): Email address to resend verification code to
    """
    email: EmailStr

class VerifyEmailRequest(BaseModel):
    """
    Request model for email verification.
    
    Attributes:
        email (EmailStr): Email address to verify
        code (str): 6-digit verification code
    """
    email: EmailStr
    code: Annotated[str, Field(min_length=6, max_length=6, pattern=r"^\d{6}$", examples=["123456"])]

class LoginRequest(BaseModel):
    """
    Request model for user login.
    
    Attributes:
        email (EmailStr): User's email address
        password (str): User's password
    """
    email: EmailStr
    password: str
