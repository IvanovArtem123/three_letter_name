from __future__ import annotations

from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, StringConstraints
from pydantic.config import Extra

from core.constants import (
    MIN_PATH_SCHEME, MAX_PATH_SCHEME, MIN_DOMAIN_SCHEME,
    MAX_DOMAIN_SCHEME, MAX_COUNTRY_SCHEME
)


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


class PanelShortInfo(BaseModel):
    """Краткая информация о панели."""
    id: int
    path: PathPanelStr
    domain: DomainPanelStr
    port: str
    country: CountryPanelStr

    model_config = ConfigDict(from_attributes=True)


class PanelCreate(BaseModel):
    """Схема для добавления новой панели."""

    path: PathPanelStr
    domain: DomainPanelStr
    port: str
    login: Annotated[str, StringConstraints(min_length=1, max_length=150)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    country: CountryPanelStr

    model_config = ConfigDict(extra=Extra.forbid)


class PanelUpdate(BaseModel):
    """Схема для обновления данных о панели."""
    path: Optional[PathPanelStr] = None
    domain: Optional[DomainPanelStr] = None
    port: Optional[str] = None
    login: Optional[
        Annotated[str, StringConstraints(min_length=1, max_length=150)]] = None
    password: Optional[
        Annotated[str, StringConstraints(min_length=1, max_length=255)]] = None
    country: Optional[CountryPanelStr] = None

    model_config = ConfigDict(extra=Extra.forbid)


class PanelInfo(PanelShortInfo):
    """Полная информация о панели."""
    login: Annotated[str, StringConstraints(min_length=1, max_length=150)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=255)]

    model_config = ConfigDict(from_attributes=True)
