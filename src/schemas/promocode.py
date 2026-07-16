from __future__ import annotations
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, StringConstraints
from pydantic.config import Extra

from .constants import PROMOCODE_MIN_LEN, PROMOCODE_MAX_LEN


CodeStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=PROMOCODE_MIN_LEN,
        max_length=PROMOCODE_MAX_LEN,
    ),
]


class PromocodeCreate(BaseModel):
    """Схема для создания промокода."""

    is_active: bool
    code: Optional[CodeStr] = None
    usage_limit: Optional[int] = 1
    purpose: Optional[int] = 0
    end_date: Optional[str] = None
    target_user_ids: Optional[list[int]] = None

    model_config = ConfigDict(extra=Extra.forbid)


class PromocodeShortInfo(BaseModel):
    """Краткая информация о промокоде."""

    id: int
    user_id: int
    code: str
    subscription_id: Optional[int] = None
    purpose: int
    end_date: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PromocodeInfo(PromocodeShortInfo):
    """Схема для отображения информации о промокоде."""

    is_active: bool
    is_disposable: bool
    usage_limit: int
    used_count: int

    model_config = ConfigDict(from_attributes=True)
