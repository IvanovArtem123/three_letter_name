from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.start import start_keyboard
from services.user import UserService
from .utils import ServiceCallback

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, session, state: FSMContext):
    if message.from_user is None:
        await message.answer('Не удалось определить пользователя.'
                             ' Попробуйте позже.')
        return
    manage_user = UserService(
        user_tg_id=message.from_user.id,
        username_tg=message.from_user.username,
        client_session=session)
    user = await manage_user.get_user()
    if user == 404:
        await manage_user.create_user()
    await state.set_state(ServiceCallback.start_menu)
    await state.update_data(
        return_text='Привет! Тебе нужен VPN? Тогда Saul Goodman поможет тебе!',
        return_keyboard=start_keyboard()
    )
    await message.answer(
        text='Привет! Тебе нужен VPN? Тогда Saul Goodman поможет тебе!',
        reply_markup=start_keyboard()
    )
