"""
Refresh token model module defining the database schema for refresh tokens.
This module contains the SQLAlchemy model for storing refresh tokens used in JWT authentication.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from datetime import datetime, timezone
from backend.app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.models.user import User


class RefreshToken(Base):
    """
    Refresh token model for storing JWT refresh tokens.
    
    Attributes:
        id (int): Primary key and unique identifier
        token (str): The refresh token string
        user_id (int): Foreign key to the user who owns this token
        created_at (datetime): Token creation timestamp
        updated_at (datetime): Last update timestamp
        user (User): Associated user object
    """
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
