from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def help_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура помощи.'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Инстркция для iPhone", callback_data="iphone_help")],
            [InlineKeyboardButton(text="Инстркция для Android", callback_data="android_help")],
            [InlineKeyboardButton(text="Инстркция для Windows", callback_data="win_help")],
            [InlineKeyboardButton(text="Инстркция для MacOS", callback_data="macos_help")],
            [InlineKeyboardButton(text="Инстркция для Linux", callback_data="linux_help")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")],
        ]
    )