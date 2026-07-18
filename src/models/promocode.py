from enum import IntEnum
from sqlalchemy import (Column, ForeignKey, String, Boolean, Integer, DateTime,
                        ARRAY)
from sqlalchemy.orm import relationship, validates

from .base import BaseModel
from .constants import MAX_LEN_PROMOCODE


class PromocodePurpose(IntEnum):
    '''Назначения промокода.'''

    GIFT_SUBSCRIPTION = 0
    DISCOUNT = 1
    REFERRAL = 2

    @classmethod
    def get_all_status(cls) -> list[int]:
        return [item.value for item in cls]


class Promocode(BaseModel):
    '''МОдель промокода.'''
    code = Column(String(MAX_LEN_PROMOCODE), nullable=False, unique=True,
                  index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    # активен / неактивен
    is_activated = Column(Boolean, nullable=False, default=False, index=True)
    purpose = Column(Integer, nullable=False,
                     default=PromocodePurpose.DISCOUNT.value)
    # назначение промокода
    end_date = Column(DateTime, nullable=True)
    # дата окончания действия промокода
    used_count = Column(Integer, default=0)
    sub_id = Column(Integer, ForeignKey('subscription.id', ondelete='CASCADE'),
                    nullable=True, index=True)
    # количество использований
    usage_limit = Column(Integer, default=0, nullable=True)
    # лимит использований
    sub_level = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'),
                     nullable=True, index=True)
    # ID пользователя, который создал промокод
    target_user_ids = Column(
        ARRAY(Integer), default=None, nullable=True
        )   # type: ignore
    user = relationship(
        'User',
        back_populates='promocodes'
    )

    @validates('code')
    def convert_upper(self, key, value):
        '''Автоматически преобразует промокод в верхний регистр'''
        if isinstance(value, str):
            return value.upper()
        return value
