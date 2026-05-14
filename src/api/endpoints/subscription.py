from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session

from schemas.subscription import (
    SubscriptionCode,
    SubscriptionInfo,
    SubscriptionCreate,
    SubscriptionShortInfo)
from crud.subscription import sub_crud

from models.user import User

from api.exceptions import forbidden
from api.validators.user import get_user_or_404
from api.validators.panel import panels_list_or_404
from api.validators.subscription import (check_headers, sub_or_404,
                                         check_exist_sub_to_user,)
from api.keys import AddUserToInbounds
from api.validators.user import check_current_user_admin
from api.services import get_current_user
from core.constants import FAKE_KEY

router = APIRouter(prefix='/sub', tags=['Подписки'])


@router.post(
    '/create',
    response_model=SubscriptionCode,
    status_code=status.HTTP_200_OK,
    summary='Создание подписки'
)
async def create_subscription(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    obj_in: SubscriptionCreate
) -> SubscriptionCode:
    """Создание подписки для пользователя.
    Для конкретного пользователя или админа."""
    if not (await check_current_user_admin(user) or user.id == obj_in.user_id):
        return forbidden('У вас недостаточно прав для создания '
                         'подписки для другого пользователя. '
                         'Вы можете создать подписку только для себя.')
    if obj_in.is_trial:
        obj_in.end_date_level = 1
    all_panels = await panels_list_or_404(session=session)  # пока все панели
    user_in_sub = await get_user_or_404(
        session=session, user_id=obj_in.user_id)
    await check_exist_sub_to_user(session=session, user_id=obj_in.user_id)
    new_sub = await sub_crud.create_subscription(
        session=session, obj_in=obj_in, panels=all_panels)
    obj = AddUserToInbounds(
        session=session,
        user=user_in_sub,
        sub=new_sub
    )
    await obj.add_user_to_inbounds()
    return SubscriptionCode(
        code=new_sub.code
        )


@router.get(
    '/get_all',
    response_model=List[SubscriptionShortInfo],
    status_code=status.HTTP_200_OK,
    summary='Получение всех подписок',
    dependencies=[Depends(get_current_user)]
)
async def get_all_sub(
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session)
) -> List[SubscriptionShortInfo]:
    '''Получение всех подписок для юзера его. Для админов все'''
    if not await check_current_user_admin(user):
        return await sub_crud.get_all(
            session=session, user_id=user.id)
    return await sub_crud.get_all(session=session)


@router.get(
    '/{sub_code}',
    response_model=SubscriptionInfo,
    status_code=status.HTTP_200_OK,
    summary='Получение всех ключей пользователя по коду подписки',
)
async def get_keys_by_sub_code(
    request: Request,
    sub_code: Annotated[str, Path(description='Код подписки')],
    session: AsyncSession = Depends(get_async_session)
) -> SubscriptionInfo:
    """Получение всех ключей пользователя по коду подписки."""
    sub = await sub_or_404(
        sub_code=sub_code,
        session=session
    )
    user = await get_user_or_404(session=session, user_id=sub.user_id)
    obj = AddUserToInbounds(
        session=session,
        user=user,
        sub=sub
    )
    if await check_headers(request=request):
        encoded_keys = await obj.get_keys_by_subid()
    if not await check_headers(request=request):
        encoded_keys = FAKE_KEY
    return PlainTextResponse(
        content=encoded_keys,
        headers={
            'Content-Type': 'text/plain; charset=utf-8',
            'Profile-Title': 'Soul Goodman VPN',
            'Subscription-Userinfo': f'expire={int(sub.end_date.timestamp())}'
        })


@router.delete(
    '/delete/{sub_code}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление подписки по коду',
    dependencies=[Depends(get_current_user)]
)
async def delete_subscription_by_sub_code(
    sub_code: Annotated[str, Path(description='Код подписки')],
    session: AsyncSession = Depends(get_async_session)
):
    '''Удаление подписки по коду.'''
    sub = await sub_or_404(
        sub_code=sub_code,
        session=session
    )
    user = await get_user_or_404(session=session, user_id=sub.user_id)
    obj = AddUserToInbounds(
        session=session,
        user=user,
        sub=sub)
    await obj.delete_client_by_subid()
    await sub_crud.delete(session=session, db_obj=sub)
