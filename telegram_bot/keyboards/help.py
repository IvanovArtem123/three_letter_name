from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def help_keyboard() -> InlineKeyboardMarkup:
    ''''Клавиатура помощи.'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Инструкции по подключению",
                                  callback_data="instructions")],
            [InlineKeyboardButton(text="Чат поддержки",
                                  url="https://t.me/saul_goodman_support")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")],
        ]
    )


def instructions_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура инструкций.'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍏 Инструкция для iPhone",
                                  callback_data="iphone_help")],
            [InlineKeyboardButton(text="📱 Инструкция для Android",
                                  callback_data="android_help")],
            [InlineKeyboardButton(text="💻 Инструкция для Windows",
                                  callback_data="win_help")],
            [InlineKeyboardButton(text="🍎 Инструкция для MacOS",
                                  callback_data="macos_help")],
            [InlineKeyboardButton(text="🐧 Инструкция для Linux",
                                  callback_data="linux_help")],
            [InlineKeyboardButton(text="⬅️ Назад",
                                  callback_data="cancel")],
        ]
    )
