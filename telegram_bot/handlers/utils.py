from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ServiceCallback(StatesGroup):
    start_menu = State()

    new_sub_menu = State()
    pay_sub_menu = State()
    price_list_menu = State()
    manage_sub_menu = State()
    promocodes_menu = State()
    promo_price_list_menu = State()

    help_menu = State()
    support_chat_menu = State()
    instructions_menu = State()

    def __init__(self, callback: CallbackQuery, state: FSMContext):
        self.callback = callback
        self.state = state

    async def service_callback(self, menu: State) -> Optional[Message]:
        '''Универсальный обработчик для перехода в меню
           с сохранением истории'''
        await self.callback.answer()
        if isinstance(self.callback.message, InaccessibleMessage
                      ) or self.callback.message is None:
            await self.callback.answer("Сообщение недоступно", show_alert=True)
            return None
        data = await self.state.get_data()
        history = data.get('history', [])
        current_state = await self.state.get_state()
        if current_state:
            history.append({
                'state': current_state,
                'text': self.callback.message.text,
                'keyboard': self.callback.message.reply_markup
            })
        await self.state.update_data(
            history=history,
            return_text=self.callback.message.text,
            return_keyboard=self.callback.message.reply_markup
        )
        await self.state.set_state(menu)
        return self.callback.message

    async def go_back(self) -> bool:
        '''Возврат на предыдущий уровень'''
        data = await self.state.get_data()
        history = data.get('history', [])
        if not history:
            return False
        prev = history.pop()
        await self.state.update_data(history=history)
        await self.callback.message.edit_text(
            prev['text'],
            reply_markup=prev['keyboard']
        )
        await self.state.set_state(prev['state'])
        return True
