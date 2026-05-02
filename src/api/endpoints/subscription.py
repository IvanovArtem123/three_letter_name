from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from api.services import get_current_user
from schemas.subscription import (
    SubscriptionCode,
    SubscriptionInfo,
    SubscriptionCreate)
from crud.subscription import sub_crud
from crud.panel import panel_crud
from api.validators.user import get_user_or_404
from api.keys import GetKeys, AddUserToInbpounds


router = APIRouter(prefix='/sub', tags=['Подписки'])


@router.post(
    '/create',
    response_model=SubscriptionCode,
    status_code=status.HTTP_200_OK,
    summary='Создание подписки',
)
async def create_subscription(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    obj_in: SubscriptionCreate
) -> SubscriptionCode:
    """Создание подписки для пользователя."""
    user = await get_user_or_404(session=session, user_id=obj_in.user_id)
    all_panels = await panel_crud.get_all(session) #  пока все панели 
    new_sub = await sub_crud.create_subscription(
        session=session, obj_in=obj_in, panels=all_panels)
    obj = AddUserToInbpounds(
        session=session,
        user=user,
        sub=new_sub
    )
    status_code = await obj.add_user_to_inbounds()
    return SubscriptionCode(
        code=new_sub.code,
        status_code=status_code
        )


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
    subscription = await sub_crud.get_subscription_by_sub_code(
        sub_code=sub_code,
        session=session
    )
    user_id = subscription.user_id
    get_keys_object = GetKeys(
        user_id=user_id,
        session=session
    )
    keys = await get_keys_object.get_keys()
    return SubscriptionInfo(
        id=subscription.id,
        user_id=subscription.user_id,
        keys=keys,
        code=subscription.code,
        end_date=subscription.end_date,
        status=subscription.status,
        created_at=subscription.created_at
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
    """Удаление подписки по коду."""
    subscription = await sub_crud.get_subscription_by_sub_code(
        sub_code=sub_code,
        session=session
    )
    await sub_crud.delete(session=session, db_obj=subscription)
