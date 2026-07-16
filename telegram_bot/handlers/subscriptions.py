from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from services.subscription import SubscriptionService

from texts.subscription import (TEXT_NEW_SUB, TEXT_PAY_SUB,
                                build_manage_sub_text)

from keyboards.default import kb_cancel
from keyboards.subscription import new_sub_keyboard
from aiogram.fsm.context import FSMContext
from .utils import ServiceCallback

router = Router()


@router.callback_query(F.data == "new_sub")
async def cb_new_sub(callback: CallbackQuery, state: FSMContext):
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.new_sub_menu)
    if message is None:
        return
    await message.edit_text(TEXT_NEW_SUB, reply_markup=new_sub_keyboard())


@router.callback_query(F.data == "pay_sub")
async def cd_pa_sub(callback: CallbackQuery, state: FSMContext):
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.pay_sub_menu)
    if message is None:
        return
    await message.edit_text(TEXT_PAY_SUB,
                            reply_markup=new_sub_keyboard())


@router.callback_query(F.data == "manage_sub")
async def cb_manage_sub(callback: CallbackQuery, session, state: FSMContext):
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.manage_sub_menu)
    if message is None:
        return
    manage_user = SubscriptionService(user_tg_id=callback.from_user.id,
                                      client_session=session)
    user_subs_data = await manage_user.get_user_subscriptions()
    if not user_subs_data:
        await message.edit_text("У вас нет активных подписок.")
    else:
        trial_subs = []
        gift_subs = []
        user_subs = []
        for sub in user_subs_data:
            if sub['is_trial'] is True:
                trial_subs.append(sub)
            if sub['is_gift'] is True:
                gift_subs.append(sub)
            elif sub['is_gift'] is False and sub['is_trial'] is False:
                user_subs.append(sub)
        text = await build_manage_sub_text(
            trial_subs=trial_subs,
            gift_subs=gift_subs,
            user_subs=user_subs)
        await message.edit_text(text, parse_mode="HTML",
                                reply_markup=kb_cancel())
    await callback.answer()


@router.callback_query(F.data.startswith("new_sub:"))
async def callback_new_sub(callback: types.CallbackQuery, state: FSMContext,
                           session):
    service_callback = ServiceCallback(callback, state)
    message = await service_callback.service_callback(
        ServiceCallback.price_list_menu)
    if message is None:
        return
    end_date_level = int(callback.data.split(":")[1])
    manage_user = SubscriptionService(user_tg_id=callback.from_user.id,
                                      client_session=session)
    user_info = await manage_user.create_sub(
        end_date_level=end_date_level)
    if user_info == 409:
        subs_user = await manage_user.get_user_subscriptions()
        await message.edit_text(f"У вас уже есть "
                                f"подписка:"
                                f"\n<code>{subs_user[0]['sub_link']}</code>",
                                parse_mode="HTML", reply_markup=kb_cancel())
    elif not user_info:
        await message.edit_text("Не удалось создать новую подписку.",
                                reply_markup=kb_cancel())
    else:
        await message.edit_text(
            f"Ваша новая подписка:\n<code>{user_info['sub_link']}</code>",
            parse_mode="HTML", reply_markup=kb_cancel())
    await callback.answer()
