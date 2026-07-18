from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.services import get_current_user, making_promocode
from core.db import get_async_session
from schemas.promocode import (PromocodeCreate, PromocodeShortInfo,
                               PromocodeInfo)
from models.user import User
from crud.promocode import promocode_crud
from api.validators.promocode import check_data_promocode, get_promo_or_404


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
    promocode = await get_promo_or_404(session, promocode_id)
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
) -> PromocodeShortInfo:
    '''Активация промокода'''
