from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.database import get_db
from app.core.security import hash_password
from app.utils.email_verification import create_and_store_verification_code
from app.core.mail_config import send_verification_email
from app.schemas.auth import ResendVerificationCodeRequest
from app.schemas.auth import VerifyEmailRequest
from datetime import datetime, timezone
from app.models.verification_code import VerificationCode


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send verification email
    code = create_and_store_verification_code(new_user.id, db)
    await send_verification_email(new_user.email, code)

    return {
        "message": "User registered successfully. Please check your email to verify your account.",
        "user_id": new_user.id
    }


@router.get("/test-send-email/{user_id}")
async def test_send_email(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    code = create_and_store_verification_code(user.id, db)
    await send_verification_email(user.email, code)

    return {"message": f"Verification code sent to {user.email}"}


@router.post("/resend-code")
async def resend_verification_code(
    payload: ResendVerificationCodeRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified")

    code = create_and_store_verification_code(user.id, db)
    await send_verification_email(user.email, code)

    return {"message": "A new verification code has been sent to your email"}


@router.post("/verify-email")
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified")

    # Find matching unused and unexpired code
    verification_code = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.user_id == user.id,
            VerificationCode.code == payload.code,
            VerificationCode.is_used == False,
            VerificationCode.expires_at > datetime.now(timezone.utc)
        )
        .order_by(VerificationCode.created_at.desc())
        .first()
    )

    if not verification_code:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    # Mark user as verified and code as used
    user.is_verified = True
    verification_code.is_used = True

    db.commit()

    return {"message": "Email verified successfully"}