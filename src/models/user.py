from sqlalchemy import (Column, Integer, String,
                        UniqueConstraint, BigInteger, Boolean)
import uuid
from enum import IntEnum
from sqlalchemy.orm import relationship

from .base import BaseModel
from core.constants import (
    USERNAME_MAX,
    EMAIL_MAX,
    )


class UserRole(IntEnum):
    '''Роль пользователя.'''

    USER = 0
    ADMIN = 1
    SUPER_USER = 2


class User(BaseModel):
    __table_args__ = (
        UniqueConstraint('email', name='uq_users_email'),
        UniqueConstraint('google_id', name='uq_users_google_id'),
    )

    subscriptions = relationship(
        'Subscription',
        backref='user',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    role = Column(Integer, nullable=False, default=int(UserRole.USER))
    uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()))
    username = Column(String(USERNAME_MAX), unique=True, nullable=False)
    email = Column(String(EMAIL_MAX), unique=True, nullable=True)
    google_id = Column(String(255), unique=True, nullable=True)
    tg_id = Column(BigInteger, unique=True, nullable=True)
    new = Column(Boolean, nullable=False, default=True)
    promocodes = relationship(
        'Promocode',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
