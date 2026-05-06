from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session

from schemas.subscription import (
    SubscriptionCode,
    SubscriptionInfo,
    SubscriptionCreate,
    SubscriptionShortInfo)
from crud.subscription import sub_crud
from crud.panel import panel_crud

from models.user import User

from api.exceptions import forbidden
from api.validators.user import get_user_or_404
from api.validators.panel import panels_list_or_404
from api.validators.subscription import sub_or_404, chek_exist_sub_to_user
from api.keys import AddUserToInbounds
from api.validators.user import check_current_user_admin_or_SU
from api.services import get_current_user

router = APIRouter(prefix='/sub', tags=['Подписки'])


@router.post(
    '/create',
    response_model=SubscriptionCode,
    status_code=status.HTTP_200_OK,
    summary='Создание подписки',
)
async def create_subscription(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    obj_in: SubscriptionCreate
) -> SubscriptionCode:
    """Создание подписки для пользователя."""
    all_panels = await panels_list_or_404(session=session)  #  пока все панели
    await chek_exist_sub_to_user(session=session, user_id=user.id)
    new_sub = await sub_crud.create_subscription(
        session=session, obj_in=obj_in, panels=all_panels)
    obj = AddUserToInbounds(
        session=session,
        user=user,
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
    '''Получение всех подписок только для адмэнов.'''
    if not await check_current_user_admin_or_SU(user):
        return forbidden(
            'У вас недостаточно прав для получения всех подписок.'
            )
    all_sub = await sub_crud.get_all(session=session)
    return all_sub


@router.get(
    '/{sub_code}',
    response_model=SubscriptionInfo,
    status_code=status.HTTP_200_OK,
    summary='Получение всех ключей пользователя по коду подписки',
    dependencies=[Depends(get_current_user)]
)
async def get_keys_by_sub_code(
    sub_code: Annotated[str, Path(description='Код подписки')],
    session: AsyncSession = Depends(get_async_session)
) -> SubscriptionInfo:
    """Получение всех ключей пользователя по коду подписки."""
    sub = await sub_crud.get_subscription_by_sub_code(
        sub_code=sub_code,
        session=session
        )
    user = await get_user_or_404(session=session, user_id=sub.user_id)
    obj = AddUserToInbounds(
        session=session,
        user=user,
        sub=sub
    )
    keys = await obj.get_keys_to_subscriprion()
    return SubscriptionInfo(
        id=sub.id,
        user_id=sub.user_id,
        keys=keys,
        code=sub_code,
        created_at=sub.created_at,
        end_date=sub.end_date,
        status=sub.status
    )


@router.delete(
    '/{sub_code}',
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
    await obj.delete_client()
    await sub_crud.delete(session=session, db_obj=sub)
