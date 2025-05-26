from fastapi import APIRouter, Depends
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/home")
def user_home(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.full_name}!"}
