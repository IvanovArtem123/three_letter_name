# services/user.py
from typing import Optional
from aiohttp import ClientSession
from services.base import BaseAPIClient
from base import logger


class UserService(BaseAPIClient):
    """Сервис для работы с пользователями."""

    def __init__(
        self,
        user_tg_id: int,
        client_session: ClientSession,
        username_tg: Optional[str] = None
    ):
        super().__init__(client_session)
        self.user_tg_id = user_tg_id
        self.username_tg = username_tg
        self.email = f"{self.user_tg_id}@tg_pass.soul"

    async def get_user(self) -> dict | int | None:
        try:
            async with self.client_session.get(
                f"{self.BACKEND_URL}/api/users/get_by_tg_id/{self.user_tg_id}",
                headers=self._get_headers(),
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return 404
                else:
                    logger.error(f"Ошибка при получении "
                                 f"пользователя: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Исключение при получении пользователя: {e}")
            return None

    async def create_user(self) -> dict | None:
        try:
            async with self.client_session.post(
                f"{self.BACKEND_URL}/api/users/login_tg",
                json={
                    "tg_id": self.user_tg_id,
                    "username": self.username_tg,
                    "email": self.email
                },
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка при создании "
                                 f" пользователя: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Исключение при создании пользователя: {e}")
            return None

    async def get_current_user_info(self) -> dict | None:
        try:
            async with self.client_session.get(
                f"{self.BACKEND_URL}/api/users/me",
                headers=self._get_headers(self.user_tg_id),
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(
                        f"Ошибка при получении информации о "
                        f"пользователе: {response.status}"
                    )
                    return None
        except Exception as e:
            logger.error(f"Исключение при получении "
                         f"информации о пользователе: {e}")
            return None

    async def get_or_create_user(self) -> Optional[dict]:
        user = await self.get_user()
        if isinstance(user, int) and user == 404:
            return await self.create_user()
        return user if isinstance(user, dict) else None
