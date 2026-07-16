# error_handlers.py
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
import logging

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"Ошибка в хендлере: {e}", exc_info=True)
            try:
                if hasattr(event, 'message') and event.message:
                    await event.message.answer("⚠️ Произошла ошибка."
                                               " Попробуйте позже.")
                elif hasattr(event, 'callback_query') and event.callback_query:
                    await event.callback_query.answer("⚠️ Произошла ошибка",
                                                      show_alert=True)
            except Exception:
                pass
            return None
