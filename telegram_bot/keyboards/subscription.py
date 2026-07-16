from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def manage_new_sub_trial_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура при покупке подписки, пробная подписка доступна.'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Активировать пробную подписку",
                                  callback_data="trial_activate")],
            [InlineKeyboardButton(text="💳 Купить подписку себе",
                                  callback_data="pay_sub")],
            [InlineKeyboardButton(text="🎁 Подарить подписку",
                                  callback_data="give_sub")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")],
        ]
    )


def price_list_keyboard() -> InlineKeyboardMarkup:
    '''Клавиатура с прайс-листом подписок.'''
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день | 15 руб.",
                              callback_data="promo:1")],
        [InlineKeyboardButton(text="1 неделя | 89 руб.",
                              callback_data="promo:2")],
        [InlineKeyboardButton(text="1 месяц | 250 руб.",
                              callback_data="promo:3")],
        [InlineKeyboardButton(text="3 месяца | 689 руб.",
                              callback_data="promo:4")],
        [InlineKeyboardButton(text="6 месяцев | 1199 руб.",
                              callback_data="promo:5")],
        [InlineKeyboardButton(text="1 год | 1890 руб.",
                              callback_data="promo:6")],
        [InlineKeyboardButton(text="⬅️ Назад",
                              callback_data="cancel")],
    ])


def new_sub_keyboard() -> InlineKeyboardMarkup:
    '''Прайс лист создания подписки.'''
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день | 15 руб.",
                              callback_data="new_sub:1")],
        [InlineKeyboardButton(text="1 неделя | 89 руб.",
                              callback_data="new_sub:2")],
        [InlineKeyboardButton(text="1 месяц | 250 руб.",
                              callback_data="new_sub:3")],
        [InlineKeyboardButton(text="3 месяца | 689 руб.",
                              callback_data="new_sub:4")],
        [InlineKeyboardButton(text="6 месяцев | 1199 руб.",
                              callback_data="new_sub:5")],
        [InlineKeyboardButton(text="1 год | 1890 руб.",
                              callback_data="new_sub:6")],
        [InlineKeyboardButton(text="ПРОМОКОД",
                              callback_data="promo_code"),
         InlineKeyboardButton(text="🎁 Подарить подписку",
                              callback_data="give_sub")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel")],
    ])
