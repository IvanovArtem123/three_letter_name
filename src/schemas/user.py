from datetime import datetime
from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    StringConstraints,
    field_validator,
    field_serializer,
)

from models.user import UserRole
from core.constants import PHONE_MAX, TG_ID_MAX, USERNAME_MAX

UsernameStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, max_length=USERNAME_MAX),
]
PhoneStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, max_length=PHONE_MAX),
]
TgIdStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, max_length=TG_ID_MAX),
]


class UserShortInfo(BaseModel):
    """Сокращённая информация о пользователе."""

    id: int
    username: str
    uuid: str
    email: Optional[EmailStr] = None
    tg_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserInfo(UserShortInfo):
    """Полная информация о пользователе."""

    role: UserRole
    created_at: datetime
    updated_at: datetime

    @field_serializer('role')
    def serialize_role(self, role: UserRole) -> str:
        return role.name.lower()


class UserUpdate(BaseModel):
    """Модель для частичного обновления пользователя."""
    tg_id: str
    role: Optional[UserRole] = None

    @field_validator('tg_id')
    @classmethod
    def _empty_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None
