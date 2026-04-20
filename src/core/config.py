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


settings = Settings()
"""Экземпляр настроек для использования в проекте."""
