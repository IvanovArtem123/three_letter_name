import uuid

from enum import IntEnum
from sqlalchemy import (Column, DateTime, Integer, ForeignKey, CheckConstraint,
                        String, Boolean)
from sqlalchemy.orm import relationship

from .base import BaseModel
from .many_to_many import subscription_panels


class SubscriptionStatus(IntEnum):
    '''Статусы подписки.'''

    NON_ACTIVE = 0
    ACTIVE = 1
    FRIZED = 2

    @classmethod
    def get_all_status(cls) -> list[int]:
        return [item.value for item in cls]


class Subscription_Date_Levels(IntEnum):
    '''Уровни даты подписки.'''

    DAY = 1
    WEEK = 2
    MONTH = 3
    THREE_MONTHS = 4
    HALF_YEAR = 5
    YEAR = 6

    @classmethod
    def get_all_levels(cls) -> list[int]:
        return [item.value for item in cls]


class Subscription(BaseModel):
    '''Модель пользовательской подписки.'''

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    end_date = Column(DateTime(timezone=True), nullable=True)
    panels = relationship(
        'Panel',
        secondary=subscription_panels,
        back_populates='subscriptions',
        lazy='selectin'
    )
    code = Column(
        String(16),
        unique=True,
        nullable=False,
        default=lambda: uuid.uuid4().hex[:16]
    )
    status = Column(
        Integer,
        nullable=False,
        default=SubscriptionStatus.ACTIVE.value,
    )
    is_trial = Column(
        Boolean,
        nullable=False,
        default=False
    )
    is_gift = Column(
        Boolean,
        nullable=False,
        default=False
    )

    __table_args__ = (
        CheckConstraint(
            'end_date IS NULL OR "end_date" > created_at',
            name='check_end_valid'
        ),
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
