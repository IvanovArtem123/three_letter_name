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


class UserShortInfo(BaseModel):
    """Сокращённая информация о пользователе."""

    id: int
    username: str
    uuid: str
    email: str
    tg_id: Optional[int] = None
    new: bool

    model_config = ConfigDict(from_attributes=True)


class TelegramLoginSchema(BaseModel):
    """Модель для создания пользователя."""
    username: UsernameStr
    tg_id: int
    email: str


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
    new: Optional[bool] = None
    tg_id: Optional[int] = None
    role: Optional[UserRole] = None
