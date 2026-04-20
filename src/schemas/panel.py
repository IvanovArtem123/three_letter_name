from __future__ import annotations

from datetime import datetime
from typing import Annotated, List, Set
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from pydantic.config import Extra

from core.constants import (
    MIN_LEN_PATH_SCHEME, MAX_LEN_PATH_SCHEME, MIN_LEN_DOMAIN_SCHEME,
    MAX_LEN_DOMAIN_SCHEME, MAX_LEN_COUNTRY_SCHEME
)


PathPanelStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=MIN_LEN_PATH_SCHEME,
        max_length=MAX_LEN_PATH_SCHEME,
    ),
]

DomainPanelStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=MIN_LEN_DOMAIN_SCHEME,
        max_length=MAX_LEN_DOMAIN_SCHEME,
    ),
]

CountryPanelStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=MAX_LEN_COUNTRY_SCHEME,
    ),
]


class PanelShortInfo(BaseModel):
    """Краткая информация о панели."""
    id: int
    path: PathPanelStr
    domain: DomainPanelStr
    country: CountryPanelStr


class PanelCreate(BaseModel):
    """Схема для добавления новой панели."""

    path: PathPanelStr
    domain: DomainPanelStr
    login: Annotated[str, StringConstraints(min_length=1, max_length=150)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    country: CountryPanelStr

    model_config = ConfigDict(extra=Extra.forbid)


class PanelUpdate(PanelCreate):
    """Схема для обновления данных о панели."""


class PanelInfo(PanelShortInfo):
    """Полная информация о панели."""
    login: Annotated[str, StringConstraints(min_length=1, max_length=150)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=255)]
