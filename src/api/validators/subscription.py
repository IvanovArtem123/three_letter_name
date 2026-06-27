from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from models.subscription import Subscription
from models.user import User
from crud.subscription import sub_crud
from api.exceptions import not_found, conflict

from schemas.subscription import SubscriptionCreate


async def sub_or_404(
    sub_code: str,
    session: AsyncSession
) -> Subscription:
    '''Получаем подписку по коду подписки или возвращаем ошибку 404.'''
    sub = await sub_crud.get_subscription_by_sub_code(
        session=session, sub_code=sub_code
    )
    if sub is None:
        return not_found('Подписки с указанным кодом не найдено.')
    return sub


async def check_exist_sub_to_user(
        session: AsyncSession,
        obj_in: SubscriptionCreate,
        user: User
) -> None:
    '''Проверка, что у пользователя уже есть подписка.'''
    # если входная подписка пробная а new - false то отмена
    subs = await sub_crud.get_subs_by_user_id(session=session, user_id=user.id)
    if obj_in.is_trial is True and user.new is False:
        return conflict('Этому пользователю нельзя'
                        ' активировать пробную подписку')
    # если входная подписка подарок то пропускает
    if obj_in.is_gift is True:
        return None
    # если входная подписка вторая для себя то нельзя
    for sub in subs:
        if sub.is_trial is True or sub.is_gift is True:
            return None
        else:
            return conflict('У этого пользователя уже есть подписка.') 
    return None


async def check_headers(
    request: Request
) -> bool:
    '''Проверка заголовокв запроса,
    чтобы только при нужных заголовках возвращался True.'''
    headers = dict(request.headers)
    user_agent = headers.get("user-agent")
    x_app_version = headers.get("x-app-version")
    return (
        user_agent is not None and
        x_app_version is not None and
        user_agent.startswith(f"Happ/{x_app_version}")
    )
