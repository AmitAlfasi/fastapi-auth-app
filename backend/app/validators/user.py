from typing import Any
from pydantic_core import PydanticCustomError


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
            - Must be at least 2 characters and no more than 50
            - Must contain only alphabetic characters
    """
    if not isinstance(value, str):
        raise PydanticCustomError("string_type", "Full name must be a string")
    if len(value) < 2:
        raise PydanticCustomError("full_name_length", "Full name must be at least 2 characters long")
    if len(value) > 50:
        raise PydanticCustomError("full_name_length", "Full name must not exceed 50 characters")
    if not value.replace(" ", "").isalpha():
        raise PydanticCustomError("full_name_alpha", "Full name must contain only alphabetic characters")
    return value
