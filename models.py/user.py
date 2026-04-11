from sqlalchemy import (CheckConstraint, Column, Integer, String,
                        UniqueConstraint)
import uuid

from .base import BaseModel
from schemas.user import UserRole


class User(BaseModel):
    """ORM-модель пользователя (classic Column API)."""

    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint(
            '(email IS NOT NULL) OR (phone IS NOT NULL)',
            name='ck_users_contact_required',
        ),
        UniqueConstraint('email', name='uq_users_email'),
        UniqueConstraint('phone', name='uq_users_phone'),
    )
    role = Column(Integer, nullable=False, default=int(UserRole.USER))
    uuid = Column(
        String(36),
        nullable=False,
        default=lambda: str(uuid.uuid4()).replace('-', '')
    )
    username = Column(String(150), nullable=False)
    email = Column(String(254), nullable=True)
    phone = Column(String(32), nullable=True)
    tg_id = Column(String(64), nullable=True)
    password_hash = Column(String(255), nullable=False)
