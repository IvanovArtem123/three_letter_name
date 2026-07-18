from schemas.promocode import PromocodeCreate
from api.exceptions import not_found, bad_request
from crud.promocode import promocode_crud
from models.promocode import PromocodePurpose
from models.subscription import Subscription_Date_Levels


async def check_data_promocode(promo_data: PromocodeCreate):
    '''Проверка данных о промокоде.'''
    if promo_data.purpose == PromocodePurpose.GIFT_SUBSCRIPTION:
        if promo_data.end_date:
            return bad_request('У подарочного промокода не может '
                               'быть срока действия.')
        if promo_data.usage_limit != 1:
            return bad_request('У подарочного промокода может быть '
                               'только одна активация!')
        sub_levels = Subscription_Date_Levels.get_all_levels()
        if promo_data.sub_level not in sub_levels:
            return bad_request(f'Указан не верный уровень подпсики. '
                               f'Выберите один из уровней подписки '
                               f'{sub_levels}')
    if promo_data.purpose == PromocodePurpose.DISCOUNT:
        if promo_data.end_date is None:
            return bad_request('Для скидочного промокода укажите '
                               'дату окончания действия промокода в '
                               'поле "end_date"')
        if promo_data.sub_level:
            return bad_request('У скидочного промокода не может быть '
                               'уровня подписки.')
    if promo_data.purpose == PromocodePurpose.REFERRAL:
        if promo_data.end_date:
            bad_request('У реферального промокода не может быть '
                        'срока действия.')
        if promo_data.usage_limit:
            bad_request('У реферального промокода не может ограничений на '
                        'количество использований.')
        if promo_data.sub_level:
            return bad_request('У реферального промокода не может быть '
                               'уровня подписки.')
        if promo_data.target_user_ids != []:
            return bad_request('Реферальный промокод не может быть назначен '
                               'для активации некоторыми пользователями.')



async def get_promo_or_404(session, id: int):
    '''Получение промокода по его коду или возврат ошибки 404.'''
    promocode = await promocode_crud.get(session=session, obj_id=id)
    if not promocode:
        return not_found('Промокод не найден.')
    return promocode
