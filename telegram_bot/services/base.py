import logging
import os
from aiohttp import ClientSession
from typing import Optional


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Базовый класс для работы с API бэкенда."""

    def __init__(self, client_session: ClientSession):
        self.client_session = client_session
        self.BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.TG_BOT_SECRET = os.getenv("TG_BOT_SECRET", "supersecret")

    def _get_headers(self, tg_id: Optional[int] = None) -> dict:
        """Формирует базовые заголовки для запросов."""
        headers = {"X-Bot-Secret": self.TG_BOT_SECRET}
        if tg_id:
            headers["X-TG-ID"] = str(tg_id)
        return headers
