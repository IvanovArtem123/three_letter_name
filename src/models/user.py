from sqlalchemy import (CheckConstraint, Column, Integer, String,
                        UniqueConstraint)
import uuid
from enum import IntEnum

from .base import BaseModel
from core.constants import (
    USERNAME_MAX,
    EMAIL_MAX,
    PHONE_MAX,
    TG_ID_MAX,
    PASS_HASH_MAX,
    CHECK_MAIL_FORMAT
    )


class UserRole(IntEnum):
    """Роль пользователя."""

    USER = 0
    ADMIN = 1


class User(BaseModel):
    """Модель пользователя."""

    __table_args__ = (
        CheckConstraint(
            '(email IS NOT NULL) OR (phone IS NOT NULL)',
            name='ck_users_contact_required',
        ),
        CheckConstraint(
            "username ~ '^[a-zA-Z0-9_]{3,20}$'",
            name='check_username_format'
        ),
        CheckConstraint(
            CHECK_MAIL_FORMAT,
            name='check_email_format'
        ),
        CheckConstraint(
            r"phone IS NULL OR phone ~ '^\+\d{7,15}$'",
            name='check_phone_format'
        ),
        UniqueConstraint('email', name='uq_users_email'),
        UniqueConstraint('phone', name='uq_users_phone'),
    )
    role = Column(Integer, nullable=False, default=int(UserRole.USER))
    uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    username = Column(String(USERNAME_MAX), unique=True, nullable=False)
    email = Column(String(EMAIL_MAX), unique=True, nullable=True)
    phone = Column(String(PHONE_MAX), unique=True, nullable=True)
    tg_id = Column(String(TG_ID_MAX), unique=True, nullable=True)
    password_hash = Column(String(PASS_HASH_MAX), unique=True, nullable=False)

    def __repr__(self):
        return (
            f"<User(id={self.id},"
            f"username={self.username},"
            f"email={self.email},"
            f"phone={self.phone})>")
