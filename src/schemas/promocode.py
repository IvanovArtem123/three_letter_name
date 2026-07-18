from typing import List
from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, StringConstraints, field_serializer
from pydantic.config import Extra

from .constants import PROMOCODE_MIN_LEN, PROMOCODE_MAX_LEN
from models.promocode import PromocodePurpose
from models.subscription import Subscription_Date_Levels


CodeStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=PROMOCODE_MIN_LEN,
        max_length=PROMOCODE_MAX_LEN,
    ),
]


class PromocodeCreate(BaseModel):
    '''Схема для создания промокода.'''

    is_active: bool
    purpose: int
    code: Optional[CodeStr] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = 1
    sub_level: Optional[int] = None
    target_user_ids: Optional[List[int]] = []

    model_config = ConfigDict(extra=Extra.forbid)


class PromocodeShortInfo(BaseModel):
    '''Краткая информация о промокоде.'''

    id: int
    is_active: bool
    user_id: int
    code: str
    purpose: PromocodePurpose
    end_date: Optional[datetime] = None
    target_user_ids: Optional[List[int]] = []
    sub_level: Optional[Subscription_Date_Levels] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('purpose')
    def serialize_purpose(self, purpose: PromocodePurpose) -> str:
        return purpose.name.upper()

    @field_serializer('sub_level')
    def serialize_sub_level(self, sub_level: Subscription_Date_Levels) -> str:
        return sub_level.name.upper()


class PromocodeInfo(PromocodeShortInfo):
    '''Схема для отображения информации о промокоде.'''

    is_active: bool
    usage_limit: int
    used_count: int

    model_config = ConfigDict(from_attributes=True)
