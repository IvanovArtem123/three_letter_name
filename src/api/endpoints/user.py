from typing import Annotated
from fastapi.params import Body

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.db import get_async_session
from schemas.user import UserCreate, UserShortInfo
from crud.user import user_crud
from api.exceptions import bad_request
from api.validators.user import (
    check_unique_email_username_phone_tgid,
    )

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.post(
        '/create',
        response_model=UserShortInfo,
        status_code=status.HTTP_201_CREATED,
        summary='Новый пользователь',
    )
async def create_user(
        user_in: UserCreate = Body(
                example={
                    'username': 'TestName1',
                    'password': 'TestPassword1',
                    'email': 'testmail@mail.com',
                    'phone': '+79998887766',
                    'tg_id': '123456789'
                }
            ),
        session: AsyncSession = Depends(get_async_session)
) -> UserShortInfo:
    """Создать нового пользователя."""
    await check_unique_email_username_phone_tgid(user_in, session)
    return await user_crud.create_hash_password(user_in, session)

@router.delete(
    '/delete/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалитль пользователя',
    )
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    """Удалить пользователя."""
    user = await user_crud.get(obj_id=user_id, session=session)
    if user:
        await user_crud.delete(db_obj=user, session=session)
