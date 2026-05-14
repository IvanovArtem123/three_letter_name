from pydantic import BaseModel


class KeysInfo(BaseModel):
    """Схема для получения информации о ключах пользователя."""
    keys: list[str]
