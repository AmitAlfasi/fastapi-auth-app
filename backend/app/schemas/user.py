"""
User schema module defining Pydantic models and validators for user-related data.
This module provides data validation and serialization for user registration and profile data.
"""

from pydantic import BaseModel, EmailStr, model_validator
from pydantic_core.core_schema import ValidationInfo
from backend.app.validators.password import validate_password
from backend.app.validators.user import validate_full_name
from pydantic_core import CoreSchema, core_schema
from pydantic.json_schema import JsonSchemaValue


class StrongPassword(str):
    """
    Custom string type for strong password validation.
    Implements Pydantic validation using an external validator function.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(validate_password)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, _handler) -> JsonSchemaValue:
        return {
            'type': 'string',
            'description': 'A strong password with at least 8 characters, one uppercase, one lowercase, and one number',
            'minLength': 8
        }


class FullName(str):
    """
    Custom string type for full name validation.
    Implements Pydantic validation using an external validator function.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(validate_full_name)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, _handler) -> JsonSchemaValue:
        return {
            "type": "string",
            "description": "Full name must contain only alphabetic characters and be between 2 and 50 characters",
            "minLength": 2,
            "maxLength": 50
        }


class UserCreate(BaseModel):
    """
    Pydantic model for user registration data.

    Attributes:
        email (EmailStr): User's email address
        password (StrongPassword): Validated password (min length, char mix)
        confirm_password (str): Password confirmation
        full_name (FullName): Validated full name (alphabetic, proper length)
    """
    email: EmailStr
    password: StrongPassword
    confirm_password: str
    full_name: FullName

    @model_validator(mode="after")  # type: ignore
    def validate_passwords_match(self, info: ValidationInfo) -> 'UserCreate':
        """
        Validate that the password and confirm_password fields match.

        Args:
            info (ValidationInfo): Validation context (required by Pydantic v2)

        Returns:
            UserCreate: The validated model instance

        Raises:
            ValueError: If password and confirm_password do not match
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self
