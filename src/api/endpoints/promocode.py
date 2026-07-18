from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.services import get_current_user, making_promocode
from core.db import get_async_session
from schemas.subscription import SubscriptionCreate
from schemas.promocode import (PromocodeCreate, PromocodeShortInfo,
                               PromocodeInfo)
from models.user import User
from models.promocode import PromocodePurpose
from crud.promocode import promocode_crud
from crud.subscription import sub_crud
from crud.panel import panel_crud
from api.validators.promocode import (check_data_promocode,
                                      get_promo_or_404_by_id,
                                      get_promo_or_404_by_code,
                                      check_permission_promo,
                                      check_count_usage,
                                      check_is_active_promocode)


router = APIRouter(prefix='/promocodes', tags=['Промокоды'])


@router.get(
    '/get_all',
    response_model=List[PromocodeShortInfo],
    status_code=status.HTTP_200_OK,
    summary='Получение списка промокодов'
)
async def get_promo_codes(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)]
) -> List[PromocodeInfo]:
    '''Получение списка промокодов для конкретного пользователя или админа.'''
    promocodes = await promocode_crud.get_all(session=session)
    return promocodes


@router.delete(
    '/delete/{promocode_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление промокода')
async def delete_promocode(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    promocode_id: Annotated[int, Path(title='ID промокода')]
):
    '''Удаление промокода для конкретного пользователя или админа.'''
    promocode = await get_promo_or_404_by_id(session, promocode_id)
    await promocode_crud.delete(session=session, db_obj=promocode)
    return {'message': 'Промокод успешно удален'}


@router.post(
    '/create',
    response_model=PromocodeShortInfo,
    status_code=status.HTTP_200_OK,
    summary='Создание промокода'
)
async def create_promocode(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    obj_in: PromocodeCreate
) -> PromocodeShortInfo:
    '''Создание промокода.'''
    await check_permission_promo(
        promocode_data=obj_in,
        user=user)
    if obj_in.code is None:
        obj_in.code = await making_promocode()
    await check_data_promocode(obj_in)
    promocode = await promocode_crud.create_promo(
        session=session,
        obj_in=obj_in,
        user_id=user.id
    )
    return promocode


@router.post(
    '/activate_promo_code/{promocode}',
    response_model=PromocodeShortInfo,
    status_code=status.HTTP_200_OK,
    summary='Активация промокода'
)
async def activate_promocode(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(get_current_user)],
    promocode: Annotated[str, Path(title='Code промокода')]
) -> PromocodeShortInfo:
    '''Активация промокода'''
    promocode_obj = await get_promo_or_404_by_code(
        session=session,
        code=promocode)
    await check_count_usage(promocode_obj=promocode_obj)
    await check_is_active_promocode(promocode_obj=promocode_obj)
    if promocode_obj.purpose == PromocodePurpose.GIFT_SUBSCRIPTION:
        sub_create_schema = SubscriptionCreate(
            end_date_level=promocode_obj.sub_level, user_id=user.id)
        panels = await panel_crud.get_all(session=session)
        new_sub = await sub_crud.create_subscription(
            obj_in=sub_create_schema,
            panels=panels,
            session=session
            )
    promocode_activated = await promocode_crud.activate_promocode(
            session=session, promocode=promocode_obj, sub_id=new_sub.id)
    return promocode_activated
