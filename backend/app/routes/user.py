"""
User routes module for handling user-specific operations.
This module provides endpoints for accessing user-specific data and functionality.
"""

from fastapi import APIRouter, Depends
from backend.app.models.user import User
from backend.app.dependencies.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/home")
def user_home(current_user: User = Depends(get_current_user)):
    """
    Get user's home page data.
    
    Args:
        current_user (User): Currently authenticated user
        
    Returns:
        dict: Welcome message with user's name
    """
    return {"message": f"Welcome, {current_user.full_name}!"}
