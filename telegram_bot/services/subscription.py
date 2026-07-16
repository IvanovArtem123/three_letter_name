from datetime import datetime
from typing import Optional
from constants import FORMAT_END_DATE
from aiohttp import ClientSession
from services.base import BaseAPIClient
from telegram_bot.services.user import UserService
from base import logger


async def get_current_datetime(backend_datetime: str) -> str:
    '''Переводит время с бэкенда в читаемое.'''
    dt_end_date = datetime.fromisoformat(backend_datetime.replace(
        'Z', '+00:00')).strftime(FORMAT_END_DATE)
    return dt_end_date


class SubscriptionService(BaseAPIClient):
    """Сервис для работы с подписками."""

    def __init__(
        self,
        user_tg_id: int,
        client_session: ClientSession,
        username_tg: Optional[str] = None
    ):
        super().__init__(client_session)
        self.user_tg_id = user_tg_id
        self.user_service = UserService(
            user_tg_id=user_tg_id,
            client_session=client_session,
            username_tg=username_tg
        )

    async def create_subscription(
        self,
        end_date_level: int,
        is_trial: bool = False,
        is_gift: bool = False
    ) -> dict | int | None:
        """Создаёт подписку для пользователя."""
        try:
            user = await self.user_service.get_or_create_user()
            if not user:
                logger.error("Не удалось получить или создать пользователя")
                return None
            async with self.client_session.post(
                f"{self.BACKEND_URL}/api/sub/create",
                headers=self._get_headers(self.user_tg_id),
                json={
                    "end_date_level": end_date_level,
                    "status": 1,
                    "user_id": user['id'],
                    "is_trial": is_trial,
                    "is_gift": is_gift
                },
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 409:
                    return 409
                else:
                    logger.error(f"Ошибка при создании "
                                 f"подписки: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Исключение при создании подписки: {e}")
            return None

    async def get_user_subscriptions(self) -> list:
        """Получает список всех подписок пользователя."""
        try:
            async with self.client_session.get(
                f"{self.BACKEND_URL}/api/sub/get_all",
                headers=self._get_headers(self.user_tg_id),
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка при получении "
                                 f"подписок: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Исключение при получении подписок: {e}")
            return []

    async def delete_subscription(self,
                                  subscription_code: Optional[str] = None
                                  ) -> bool:
        """Удаляет подписку пользователя."""
        try:
            if not subscription_code:
                return await self._delete_all_subscriptions()
            async with self.client_session.delete(
                f"{self.BACKEND_URL}/api/sub/delete/{subscription_code}",
                headers=self._get_headers(self.user_tg_id),
                timeout=10
            ) as response:
                if response.status == 200:
                    logger.info(f"Подписка {subscription_code} удалена")
                    return True
                else:
                    logger.error(
                        f"Ошибка при удалении "
                        f" подписки {subscription_code}: {response.status}"
                    )
                    return False
        except Exception as e:
            logger.error(f"Исключение при удалении подписки: {e}")
            return False

    async def _delete_all_subscriptions(self) -> bool:
        """Удаляет все подписки пользователя."""
        try:
            subscriptions = await self.get_user_subscriptions()
            if not subscriptions:
                logger.info("У пользователя нет активных "
                            "подписок для удаления")
                return False
            success = True
            for sub in subscriptions:
                result = await self.delete_subscription(sub['code'])
                if not result:
                    success = False
            return success
        except Exception as e:
            logger.error(f"Исключение при удалении всех подписок: {e}")
            return False

    async def has_active_subscription(self) -> bool:
        """Проверяет, есть ли у пользователя активная подписка."""
        subscriptions = await self.get_user_subscriptions()
        return bool(subscriptions)

    async def get_active_subscription(self) -> dict | None:
        """Получает первую активную подписку пользователя."""
        subscriptions = await self.get_user_subscriptions()
        return subscriptions[0] if subscriptions else None
