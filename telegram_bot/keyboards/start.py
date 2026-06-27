from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура для команды /start'''
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Приобрести подписку", callback_data="new_sub")],
        [InlineKeyboardButton(text="💼 Управление подписками", callback_data="manage_sub")],
        [InlineKeyboardButton(text="👥 Реферальная программа", callback_data="referral")],
        [InlineKeyboardButton(text="📢 Наш канал", url="https://t.me/saul_goodman_vpn"), InlineKeyboardButton(text="🆘 Помощь", callback_data="help")]
    ])
