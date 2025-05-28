import re
from typing import Any
from pydantic_core import PydanticCustomError

def validate_password(value: Any) -> str:
    """
    Validate that a password is strong.

    Requirements:
    - At least 8 characters
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one number
    """
    if not isinstance(value, str):
        raise PydanticCustomError("string_type", "Password must be a string")
    if len(value) < 8:
        raise PydanticCustomError("password_length", "Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", value):
        raise PydanticCustomError("password_uppercase", "Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise PydanticCustomError("password_lowercase", "Password must contain at least one lowercase letter")
    if not re.search(r"\d", value):
        raise PydanticCustomError("password_number", "Password must contain at least one number")
    return value
