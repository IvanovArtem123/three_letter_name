from schemas.promocode import PromocodeCreate
from api.services import making_promocode
from models.constants import MAX_LEN_PROMOCODE
from api.exceptions import bad_request
from crud.promocode import promocode_crud


async def check_promocode_data(promocode_data: PromocodeCreate) -> PromocodeCreate:
    """Проверка данных промокода в зависимости от его назначения."""
    if promocode_data.code is None: # Если код не указан, генерируем случайный промокод
        promocode_data.code = await making_promocode(MAX_LEN_PROMOCODE)
    if promocode_data.purpose == 0:
        if promocode_data.end_date:
            return bad_request('Промокод подарка не может иметь дату окончания.')   
    elif promocode_data.purpose == 1:
        if promocode_data.usage_limit is None:
            promocode_data.usage_limit = 1
    elif promocode_data.purpose == 2:
        if promocode_data.usage_limit is None:
            promocode_data.usage_limit = 1
    return promocode_data


async def get_promo_or_404(session, id: int):
    """Получение промокода по его коду или возврат ошибки 404."""
    promocode = await promocode_crud.get(session=session, id=id)
    if not promocode:
        return bad_request('Промокод не найден.')
    return promocode
