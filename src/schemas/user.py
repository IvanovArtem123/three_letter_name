from enum import IntEnum
from fastapi_users import schemas


class UserRole(IntEnum):
    """Роль пользователя."""

    USER = 0
    ADMIN = 1

class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass