from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.subscription import price_list_keyboard
from aiogram.fsm.context import FSMContext
from .utils import ServiceCallback

router = Router()


@router.callback_query(F.data == "give_sub")
async def cb_give_sub(callback: CallbackQuery, state: FSMContext):
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.promocodes_menu)
    if message is None:
        return
    await message.edit_text("Выберите срок подписки для подарка:",
                            reply_markup=price_list_keyboard())
