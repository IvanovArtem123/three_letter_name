from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from manage_users import ManageUser

from keyboards import start_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, session):
    if message.from_user is None:
        await message.answer("Не удалось определить пользователя. Попробуйте позже.")
        return
    manage_user = ManageUser(
        user_tg_id=message.from_user.id,
        username_tg=message.from_user.username,
        client_session=session)
    user = await manage_user.get_user()
    if user == 404:
        await manage_user.create_user()
    await message.answer(
        "Привет! Тебе нужен VPN? Тогда Saul Goodman поможет тебе!",
        reply_markup=start_keyboard()
    )
