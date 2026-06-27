from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from manage_users import ManageUser

router = Router()


@router.message(Command('me'))
async def cmd_me(message: Message, session):
    manage_user = ManageUser(message.from_user.id, None, session)
    user_info = await manage_user.get_current_user_info()
    if not user_info:
        await message.answer("Не удалось получить информацию о пользователе.")
    else:
        await message.answer(f"Ваша информация: {user_info}")