import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_ROOT = PROJECT_ROOT / '.env'
ENV_INFRA = PROJECT_ROOT / 'infra' / '.env'

load_dotenv(ENV_ROOT, override=False)
load_dotenv(ENV_INFRA, override=False)


@dataclass(frozen=True)
class Settings:
    """Настройки проекта."""
    app_title: str = 'SoulGoodman VPN API'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    # JWT
    SECRET: str = os.getenv('SECRET', 'CHANGE_ME_SUPER_SECRET_32CHARS_MIN')
    JWT_ALGO: str = os.getenv('JWT_ALGO', 'HS256')
    TOKEN_IDLE_TTL_MIN: int = int(os.getenv('TOKEN_IDLE_TTL_MIN', '30'))


settings = Settings()
"""Экземпляр настроек для использования в проекте."""
