from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

StrongPassword = Annotated[str, Field(
    min_length=8,
    description=(
        "Password must be at least 8 characters long, contain at least one lowercase letter, "
        "one uppercase letter, and one number."
    )
)]

FullName = Annotated[str, Field(
    max_length=50,
    description="Full name must contain only alphabetic characters and be no longer than 50 characters."
)]

class UserCreate(BaseModel):
    email: EmailStr
    password: StrongPassword
    full_name: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        return value
    
    
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not value.replace(" ", "").isalpha():
            raise ValueError("Full name must contain only alphabetic characters.")
        return value