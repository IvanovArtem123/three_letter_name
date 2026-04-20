from datetime import datetime, timezone
from enum import IntEnum
from sqlalchemy import Column, DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from .base import BaseModel
from .many_to_many import subscription_panels


class SubscriptionStatus(IntEnum):
    """Статусы подписки."""

    NON_ACTIVE = 0
    ACTIVE = 1
    FRIZED = 2


class Subscription(BaseModel):
    """Модель пользовательской подписки."""

    __tablename__ = 'subscriptions'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    end_date = Column(DateTime(timezone=True), nullable=False)
    panels = relationship(
        "Panel",
        secondary=subscription_panels,
        back_populates="subscriptions",
        lazy='selectin'
    )
    status = Column(
        Integer,
        nullable=False,
        default=SubscriptionStatus.ACTIVE.value,
    )

    __table_args__ = (
        CheckConstraint(
            'end_date IS NULL OR "end_date" > created_at',
            name='check_end_valid'
        ),
    )
