from datetime import datetime

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from manage_users import ManageUser
from keyboards import manage_new_sub_keyboard, manage_new_sub_trial_keyboard
from aiogram.types import InaccessibleMessage

from texts.subscription import (TEXT_NEW_SUB, TEXT_NEW_SUB_TRIAL,
                                             build_trial_activate_sub,
                                             build_manage_sub_text)

router = Router()


@router.callback_query(F.data == "cancel")
async def ca_cancel(callback: CallbackQuery):
    if isinstance(callback.message,
                  InaccessibleMessage) or callback.message is None:
        await callback.answer(
            "Сообщение недоступно для удаления", show_alert=True)
        return
    await callback.message.delete()
    await callback.answer("Действие отменено")


@router.callback_query(F.data == "new_sub")
async def cb_new_sub(callback: CallbackQuery, session):
    await callback.answer()
    manage_user = ManageUser(callback.from_user.id, None, session)
    user_info = await manage_user.get_user()
    if user_info['new'] == True:
        await callback.message.answer(
            TEXT_NEW_SUB_TRIAL, reply_markup=manage_new_sub_trial_keyboard())
    if user_info['new'] == False:
        await callback.message.answer(
            TEXT_NEW_SUB, reply_markup=manage_new_sub_keyboard())


@router.callback_query(F.data == "trial_activate")
async def cd_trial_sub_activate(callback: CallbackQuery, session):
    manage_user = ManageUser(callback.from_user.id, None, session)
    # создание пробной подписки и возврат информации об этой подписке
    new_trial_sub = await manage_user.create_sub(is_trial=True, end_date_level=1)
    dt_end_date = datetime.fromisoformat(
        new_trial_sub['end_date'].replace(
            'Z', '+00:00')).strftime('%H:%M %d.%m.%Y')
    text = build_trial_activate_sub(
        end_date=dt_end_date, sub_link=new_trial_sub['sub_link'])
    await callback.message.answer(
        text, parse_mode='HTML', reply_markup=manage_new_sub_keyboard())


@router.callback_query(F.data == "manage_sub")
async def cb_manage_sub(callback: CallbackQuery, session):
    await callback.answer()
    manage_user = ManageUser(callback.from_user.id, None, session)
    user_subs_data = await manage_user.get_user_subscriptions()
    if not user_subs_data:
        await callback.message.answer("У вас нет активных подписок.")
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
        await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("new_sub:"))
async def callback_new_sub(callback: types.CallbackQuery, session):
    end_date_level = int(callback.data.split(":")[1])
    manage_user = ManageUser(callback.from_user.id, None, session)
    user_info = await manage_user.create_subscription(
        end_date_level=end_date_level)
    if user_info == 409:
        subs_user = await manage_user.get_user_subscriptions()
        await callback.message.answer(f"У вас уже есть подписка: {subs_user[0]['sub_link']}")
    if not user_info:
        await callback.message.answer("Не удалось создать новую подписку.")
    else:
        await callback.message.answer(
            f"Ваша новая подписка:\n<code>{user_info['sub_link']}</code>",
            parse_mode="HTML")
    await callback.answer()

@router.message(Command("delete_sub"))
async def cmd_delete_sub(message: Message, session):
    manage_user = ManageUser(message.from_user.id, None, session)
    result = await manage_user.delete_subscription()
    if not result:
        await message.answer("Подписка успешно удалена.")
    else:
        await message.answer("У вас нет активных подписок для удаления.")

@router.message(Command("help"))
async def cmd_help(message: Message): 
    await message.answer(
        f'Доступные команды:\n'
        f'/new_sub - Создать новую подписку\n'
        f'/mysubs - Мои подписки\n'
        f'/delete_sub - Удалить подписку\n'
        f'/me - Получить информацию о себе\n'
    )
