import hashlib

from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from passlib.context import CryptContext

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings


async def hash_password(password: str) -> str:
    """Вернуть хэш для заданного пароля SHA256."""
    # SHA256 хеширование первым слоем (любая длина пароля → 64 символа)
    hash_object = hashlib.sha256(password.encode('utf-8'))
    # Затем bcrypt
    return hash_object.hexdigest()
