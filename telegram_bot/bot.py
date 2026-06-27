import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import start, subscriptions, me 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(subscriptions.router)
dp.include_router(me.router)

session: aiohttp.ClientSession = None

@dp.startup()
async def on_startup():
    global session
    session = aiohttp.ClientSession()
    # Пробрасываем сессию в хэндлеры через middleware
    dp.update.middleware(lambda handler, event, data: handler(event, {**data, "session": session}))
    logger.info("Бот запущен")

@dp.shutdown()
async def on_shutdown():
    if session:
        await session.close()
    logger.info("Бот остановлен")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())