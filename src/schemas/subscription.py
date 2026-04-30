from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from pydantic.config import Extra

from core.constants import (
    MIN_PATH_SCHEME, MAX_PATH_SCHEME, MIN_DOMAIN_SCHEME,
    MAX_DOMAIN_SCHEME, MAX_COUNTRY_SCHEME
)
from schemas.panel import PanelInfo

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


class SubscriptionCreate(BaseModel):
    user_id: int
    end_date_level: int
    status: Optional[int] = 1

    model_config = ConfigDict(extra=Extra.forbid)


class SubscriptionUpdate(BaseModel):
    end_date: datetime
    status: Optional[int] = 1

    model_config = ConfigDict(extra=Extra.forbid)


class SubscriptionGetShortInfo(BaseModel):
    id: int
    user_id: int
    keys: list[str]
    code: str
    end_date: datetime
    status: int

    model_config = ConfigDict(from_attributes=True)


class SubscriptionInfo(SubscriptionGetShortInfo):
    created_at: datetime