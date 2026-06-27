from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_cancel() -> InlineKeyboardMarkup:
    '''Кнопка назад.'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")]
        ]
    )