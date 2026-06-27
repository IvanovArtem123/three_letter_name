from services.subscription import get_current_datetime

TEXT_NEW_SUB = ('Тут можно прикупить себе подпсику или подарить подписку'
                ' другому человеку🎁')
TEXT_NEW_SUB_TRIAL = (
    'Тут можно прикупить себе подпсику или сделать подарок 🎁'
    '\n\nТак же тебе доступна пробная подписке на 1 день, нажми на кнопку'
    '"активировать подписку", чтобы подписка начала действовать ⏳')


def build_trial_activate_sub(end_date: str, sub_link: str):
    return (
        f'Ваша пробная подписка активирована, она будет действовать'
        f' 1 день, то есть до {end_date}. Ссылка на подписку: \n\n'
        f'</code>{sub_link}</code>\n\nВставьте ссылку в приложение Happ'
        )


async def build_manage_sub_text(trial_subs: list = [],
                                gift_subs: list = [],
                                user_subs: list = []):
    trial_text = ''
    if trial_subs:
        end_date = await get_current_datetime(trial_subs[0]['end_date'])
        trial_text = (
            f'Ваша пробная подписка:\n'
            f'<code>{trial_subs[0]["sub_link"]}</code>'
            f' - действительна до: {end_date}\n\n'
        )
    user_subs_text = ''
    if user_subs:
        user_subs_text = 'Ваши личные подписки:\n'
        for user_sub in user_subs:
            end_date = await get_current_datetime(user_sub['end_date'])
            user_subs_text += (
                f'<code>{user_sub["sub_link"]}</code>'
                f' - действительна до: {end_date}\n'
            )
        user_subs_text += '\n'
    gift_subs_text = ''
    if gift_subs:
        gift_subs_text = 'Ваши подарочные подписки:\n'
        for gift_sub in gift_subs:
            end_date = await get_current_datetime(gift_sub['end_date'])
            gift_subs_text += (
                f'<code>{gift_sub["sub_link"]}</code>'
                f' - действительна до: {end_date}\n'
            )
        gift_subs_text += '\n'
    result = 'Здесь можно управлять своими подписками или подарочными подписками ⚙️\n\n'
    if trial_text:
        result += trial_text
    if user_subs_text:
        result += user_subs_text
    if gift_subs_text:
        result += gift_subs_text
    if not (trial_text or user_subs_text or gift_subs_text):
        result += 'У вас нет активных подписок.'
    return result
