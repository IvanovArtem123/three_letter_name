from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional

from pydantic import (
    BaseModel, ConfigDict, StringConstraints, field_validator, model_validator)
from pydantic.config import Extra

from core.constants import (
    MIN_PATH_SCHEME, MAX_PATH_SCHEME, MIN_DOMAIN_SCHEME,
    MAX_DOMAIN_SCHEME, MAX_COUNTRY_SCHEME
)
from models.subscription import Subscription_Date_Levels, SubscriptionStatus
from core.config import settings


PathPanelStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=MIN_PATH_SCHEME,
        max_length=MAX_PATH_SCHEME,
    ),
]

DomainPanelStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=MIN_DOMAIN_SCHEME,
        max_length=MAX_DOMAIN_SCHEME,
    ),
]

CountryPanelStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=MAX_COUNTRY_SCHEME,
    ),
]


class SubscriptionUpdate(BaseModel):
    end_date_level: Optional[int] = None
    status: Optional[int] = 1

    model_config = ConfigDict(extra=Extra.forbid)

    @field_validator('end_date_level')
    def _check_range_end_date_level(cls, v: int) -> int:
        if v is None:
            return v
        list_levels_end_date = Subscription_Date_Levels.get_all_levels()
        if v not in list_levels_end_date:
            raise ValueError(f'Доступные уровни продолжительности подписки: '
                             f'{list_levels_end_date}')
        return v

    @field_validator('status')
    def _check_range_status_sub(cls, v: int) -> int:
        if v is None:
            return v
        list_status_sub = SubscriptionStatus.get_all_status()
        if v not in list_status_sub:
            raise ValueError(f'Доступные уровни статуса подписки: '
                             f'{list_status_sub}')
        return v


class SubscriptionCreate(SubscriptionUpdate):
    '''Схема создания подписки.'''
    user_id: int
    end_date_level: int
    is_trial: Optional[bool] = False
    is_gift: Optional[bool] = False

    @model_validator(mode='after')
    def _check_trial_and_gift_field(self):
        if self.is_trial is True and self.is_gift is True:
            raise ValueError('Подписка не может быть одновременно '
                             'подарочной и пробной.')
        return self


class SubscriptionShortInfo(BaseModel):
    id: int
    user_id: int
    sub_link: Optional[str] = None
    end_date: datetime
    status: int
    is_trial: bool
    is_gift: bool
    code: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def set_sub_link(self):
        if not self.sub_link and self.code:
            self.sub_link = f'{settings.BASE_URL}/api/sub/{self.code}'
        return self


class SubscriptionInfo(SubscriptionShortInfo):
    created_at: datetime
    keys: list[str]
