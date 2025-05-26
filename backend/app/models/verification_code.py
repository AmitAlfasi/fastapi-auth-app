"""
Verification code model module defining the database schema for email verification codes.
This module contains the SQLAlchemy model for storing verification codes used in email verification.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone
from backend.app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.models.user import User


class VerificationCode(Base):
    """
    Verification code model for storing email verification codes.
    
    Attributes:
        id (int): Primary key and unique identifier
        user_id (int): Foreign key to the user who owns this code
        code (str): The verification code string
        expires_at (datetime): Expiration timestamp for the code
        is_used (bool): Whether the code has been used
        created_at (datetime): Code creation timestamp
        user (User): Associated user object
    """
    __tablename__ = "verification_codes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    user: Mapped["User"] = relationship("User", back_populates="verification_codes")
