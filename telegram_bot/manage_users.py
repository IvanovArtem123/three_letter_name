import os
import logging

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class ManageUser:
    def __init__(
            self, user_tg_id: int, username_tg: str,
            client_session: ClientSession):
        self.user_tg_id = user_tg_id
        self.username_tg = username_tg
        self.email = str(self.user_tg_id) + '@tg_pass.soul'
        self.client_session = client_session
        self.BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.TG_BOT_SECRET = os.getenv("TG_BOT_SECRET", "supersecret")

    async def get_user(self):
        '''Получаем пользователя по tg id'''
        try:
            async with self.client_session.get(
                f'{self.BACKEND_URL}/api/users/get_by_tg_id/{self.user_tg_id}',
                headers={"X-Bot-Secret": self.TG_BOT_SECRET},
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return 404
        except Exception as e:
            logger.error(f"Исключение при работе с пользователем: {e}")
            return None

    async def create_user(self):
        try:
            async with self.client_session.post(
                f"{self.BACKEND_URL}/api/users/login_tg",
                json={
                    "tg_id": self.user_tg_id,
                    "username": self.username_tg,
                    "email": self.email},
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка при создании"
                                 f"пользователя: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Исключение при работе с пользователем: {e}")
            return None

    async def create_sub(
            self, end_date_level: int, is_trial: bool = False,
            is_gift: bool = False,):
        '''Создание подписки с флагами: пробная или подарочная.'''
        user = await self.get_user()
        async with self.client_session.post(
            f"{self.BACKEND_URL}/api/sub/create",
                headers={
                    "X-Bot-Secret": self.TG_BOT_SECRET,
                    "X-TG-ID": str(self.user_tg_id)},
                json={
                    "end_date_level": end_date_level,
                    "status": 1,
                    "user_id": user['id'],
                    "is_trial": is_trial,
                    "is_gift": is_gift
                    }) as response:
            if response.status == 200:
                return await response.json()
            else:
                None

    async def get_user_subscriptions(self) -> list:
        '''Получаем список подписок пользователя с бэкенда.'''
        try:
            async with self.client_session.get(
                f"{self.BACKEND_URL}/api/sub/get_all",
                headers={
                    "X-Bot-Secret": self.TG_BOT_SECRET,
                    "X-TG-ID": str(self.user_tg_id)},
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка при получении подписок: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Исключение при получении подписок: {e}")
            return []

    async def create_subscription(self, end_date_level: int) -> dict:
        '''Создаём новую подписку для пользователя.'''
        try:
            user = await self.get_or_create_user()
            async with self.client_session.post(
                f"{self.BACKEND_URL}/api/sub/create",
                headers={
                    "X-Bot-Secret": self.TG_BOT_SECRET,
                    "X-TG-ID": str(self.user_tg_id)},
                json={
                    "end_date_level": end_date_level,
                    "status": 1,
                    "user_id": user['id'],
                    "is_trial": 'false',
                    "is_gift": 'false'
                    },
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка при создании подписки: {response.status}")
                    return response.status
        except Exception as e:
            logger.error(f"Исключение при создании подписки: {e}")
            return None

    async def get_current_user_info(self) -> dict:
        '''Получаем текущую информацию о пользователе с бэкенда.'''
        try:
            async with self.client_session.get(
                f"{self.BACKEND_URL}/api/users/me",
                headers={
                    "X-Bot-Secret": self.TG_BOT_SECRET,
                    "X-TG-ID": str(self.user_tg_id)},
                timeout=10
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка при получении информации о пользователе: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Исключение при получении информации о пользователе: {e}")
            return None
        
    async def delete_subscription(self) -> bool:
        '''Удаляем активную подписку пользователя.'''
        try:
            user_subs = await self.get_user_subscriptions()
            if not user_subs:
                logger.info("У пользователя нет активных подписок для удаления.")
                return False
            for sub in user_subs:
                async with self.client_session.delete(
                    f"{self.BACKEND_URL}/api/sub/delete/{sub['code']}",
                    headers={
                        "X-Bot-Secret": self.TG_BOT_SECRET,
                        "X-TG-ID": str(self.user_tg_id)},
                    timeout=10
                ) as response:
                    if response.status == 200:
                        logger.info(f"Подписка с ID {sub['code']} успешно удалена.")
                        return True
                    else:
                        logger.error(f"Ошибка при удалении подписки с ID {sub['code']}: {response.status}")
            async with self.client_session.delete(
                f"{self.BACKEND_URL}/api/sub/delete/",
                headers={
                    "X-Bot-Secret": self.TG_BOT_SECRET,
                    "X-TG-ID": str(self.user_tg_id)},
                timeout=10
            ) as response:
                if response.status == 200:
                    return True
                else:
                    logger.error(f"Ошибка при удалении подписки: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Исключение при удалении подписки: {e}")
            return False
