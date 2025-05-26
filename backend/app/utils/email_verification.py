import random
import string
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from backend.app.models.verification_code import VerificationCode
from backend.app.models.user import User

def generate_verification_code(length: int = 6) -> str:
    """Generate a random numeric code (default: 6-digit)."""
    return ''.join(random.choices(string.digits, k=length))


def create_and_store_verification_code(user_id: int, db: Session, expires_in_minutes: int = 15) -> str:
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("User not found")
    if user.is_verified:
        raise ValueError("User is already verified")    
   
   
    # Invalidate any previous unused codes
    db.query(VerificationCode).filter(
        VerificationCode.user_id == user_id,
        VerificationCode.is_used == False
    ).update({VerificationCode.is_used: True})
    
    # Generate and save a new code
    code = generate_verification_code()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)

    verification = VerificationCode(
        user_id=user_id,
        code=code,
        expires_at=expires_at,
        is_used=False
    )
    db.add(verification)
    db.commit()
    db.refresh(verification)

    return code
