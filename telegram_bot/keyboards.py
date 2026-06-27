from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура для команды /start'''
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Приобрести подписку", callback_data="new_sub")],
        [InlineKeyboardButton(text="💼 Управление подписками", callback_data="manage_sub")],
        [InlineKeyboardButton(text="👥 Реферальная программа", callback_data="referral")],
        [InlineKeyboardButton(text="📢 Наш канал", url="https://t.me/saul_goodman_vpn"), InlineKeyboardButton(text="🆘 Помощь", callback_data="help")]
    ])


def manage_new_sub_trial_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура при покупке подписки, пробная подписка доступна.'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Активировать пробную подписку", callback_data="trial_activate")],
            [InlineKeyboardButton(text="💳 Купить подписку себе", callback_data="pay_sub")],
            [InlineKeyboardButton(text="🎁 Подарить подписку", callback_data="give_sub")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")],
        ]
    )


def manage_new_sub_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура при покупке подписки, пробная без пробной подписки.'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Купить подписку себе", callback_data="pay_sub")],
            [InlineKeyboardButton(text="🎁 Подарить подписку другому", callback_data="give_sub")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")],
        ]
    )



def help_keyboard() -> InlineKeyboardMarkup:
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


def manage_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📆 Продлить подписку", callback_data="renew_sub")],
            [InlineKeyboardButton(text="🚫 Удалить подписку", callback_data="delete_sub")],
        ]
    )


def new_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день | 15 руб.",    callback_data="new_sub:1")],
        [InlineKeyboardButton(text="1 неделя | 89 руб.",  callback_data="new_sub:2")],
        [InlineKeyboardButton(text="1 месяц | 250 руб.",   callback_data="new_sub:3")],
        [InlineKeyboardButton(text="3 месяца | 689 руб.",  callback_data="new_sub:4")],
        [InlineKeyboardButton(text="6 месяцев | 1199 руб.", callback_data="new_sub:5")],
        [InlineKeyboardButton(text="1 год | 1890 руб.",     callback_data="new_sub:6")],
        [InlineKeyboardButton(text="3 года | 4990 руб.",    callback_data="new_sub:7")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")],
    ])
