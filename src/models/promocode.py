from enum import IntEnum
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.orm import validates

from .base import BaseModel
from .constants import MAX_LEN_PROMOCODE


class PromocodePurpose(IntEnum):
    """Назначения промокода."""

    GIFT_SUBSCRIPTION = 0
    DISCOUNT = 1
    REFERRAL = 2

    @classmethod
    def get_all_status(cls) -> list[int]:
        return [item.value for item in cls]


class Promocode(BaseModel):
    code = Column(String(MAX_LEN_PROMOCODE), nullable=False, unique=True,
                  index=True)
    is_active = Column(Boolean, nullable=False, default=False, index=True)
    is_disposable = Column(Boolean, nullable=False, default=False)
    purpose = Column(Integer, nullable=False,
                     default=PromocodePurpose.DISCOUNT.value)
    end_date = Column(DateTime, nullable=True)
    used_count = Column(Integer, default=0)
    usage_limit = Column(Integer, default=1)

    @validates('code')
    def convert_upper(self, key, value):
        """Автоматически преобразует промокод в верхний регистр"""
        if isinstance(value, str):
            return value.upper()
        return value
