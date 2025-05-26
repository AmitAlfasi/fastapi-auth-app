from typing import Any
from pydantic import BaseModel, EmailStr, model_validator, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError, core_schema
import re

def validate_password(value: Any) -> str:
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
    if not isinstance(value, str):
        raise PydanticCustomError("string_type", "Full name must be a string")
    if len(value) > 50:
        raise PydanticCustomError("full_name_length", "Full name must not exceed 50 characters")
    if not value.replace(" ", "").isalpha():
        raise PydanticCustomError("full_name_alpha", "Full name must contain only alphabetic characters")
    return value

class StrongPassword(str):
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
    email: EmailStr
    password: StrongPassword
    confirm_password: str
    full_name: FullName

    @model_validator(mode="after")
    def validate_passwords_match(self) -> 'UserCreate':
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self
