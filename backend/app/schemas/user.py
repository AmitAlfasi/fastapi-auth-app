"""
User schema module defining Pydantic models and validators for user-related data.
This module provides data validation and serialization for user registration and profile data.
"""

from typing import Any
from pydantic import BaseModel, EmailStr, model_validator, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError, core_schema
import re

def validate_password(value: Any) -> str:
    """
    Validate password strength requirements.
    
    Args:
        value (Any): Password to validate
        
    Returns:
        str: Validated password
        
    Raises:
        PydanticCustomError: If password doesn't meet requirements:
            - Must be a string
            - Must contain at least one lowercase letter
            - Must contain at least one uppercase letter
            - Must contain at least one number
            - Must be at least 8 characters long
    """
    if not isinstance(value, str):
        raise PydanticCustomError(
            'string_type',
            'Value must be a string'
        )
    
    if not re.search(r"[a-z]", value):
        raise PydanticCustomError(
            'password_lowercase',
            'Password must contain at least one lowercase letter'
        )
    if not re.search(r"[A-Z]", value):
        raise PydanticCustomError(
            'password_uppercase',
            'Password must contain at least one uppercase letter'
        )
    if not re.search(r"\d", value):
        raise PydanticCustomError(
            'password_number',
            'Password must contain at least one number'
        )
    if len(value) < 8:
        raise PydanticCustomError(
            'password_length',
            'Password must be at least 8 characters long'
        )
    return value

def validate_full_name(value: Any) -> str:
    """
    Validate full name requirements.
    
    Args:
        value (Any): Full name to validate
        
    Returns:
        str: Validated full name
        
    Raises:
        PydanticCustomError: If name doesn't meet requirements:
            - Must be a string
            - Must not exceed 50 characters
            - Must contain only alphabetic characters
    """
    if not isinstance(value, str):
        raise PydanticCustomError("string_type", "Full name must be a string")
    if len(value) > 50:
        raise PydanticCustomError("full_name_length", "Full name must not exceed 50 characters")
    if not value.replace(" ", "").isalpha():
        raise PydanticCustomError("full_name_alpha", "Full name must contain only alphabetic characters")
    return value

class StrongPassword(str):
    """
    Custom string type for strong password validation.
    Implements Pydantic validation for password strength requirements.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: type, _handler: GetJsonSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(validate_password)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: CoreSchema, _handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {
            'type': 'string',
            'description': 'A strong password with at least 8 characters, one uppercase, one lowercase, and one number',
            'minLength': 8
        }

class FullName(str):
    """
    Custom string type for full name validation.
    Implements Pydantic validation for name format requirements.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(validate_full_name)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, _handler) -> JsonSchemaValue:
        return {
            "type": "string",
            "description": "Full name must contain only alphabetic characters and be no longer than 50 characters",
            "maxLength": 50
        }

class UserCreate(BaseModel):
    """
    Pydantic model for user registration data.
    
    Attributes:
        email (EmailStr): User's email address
        password (StrongPassword): User's password (must meet strength requirements)
        confirm_password (str): Password confirmation (must match password)
        full_name (FullName): User's full name (must meet format requirements)
    """
    email: EmailStr
    password: StrongPassword
    confirm_password: str
    full_name: FullName

    @model_validator(mode="after")
    def validate_passwords_match(self) -> 'UserCreate':
        """
        Validate that password and confirm_password match.
        
        Returns:
            UserCreate: The validated model instance
            
        Raises:
            ValueError: If passwords do not match
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self
