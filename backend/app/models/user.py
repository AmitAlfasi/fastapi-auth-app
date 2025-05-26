"""
User model module defining the database schema for user accounts.
This module contains the SQLAlchemy model for user data and its relationships.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime, timezone
from backend.app.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.app.models.refresh_token import RefreshToken
    from backend.app.models.verification_code import VerificationCode

class User(Base):
    """
    User model representing a user account in the system.
    
    Attributes:
        id (int): Primary key and unique identifier
        email (str): User's email address (unique)
        hashed_password (str): Securely hashed password
        full_name (str | None): User's full name (optional)
        is_verified (bool): Whether the user's email is verified
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
        refresh_tokens (list[RefreshToken]): Associated refresh tokens
        verification_codes (list[VerificationCode]): Associated verification codes
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
)

    # Relationships
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )

    verification_codes: Mapped[list["VerificationCode"]] = relationship(
        "VerificationCode", back_populates="user", cascade="all, delete-orphan"
    )
