from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from schemas.panel import PanelCreate, PanelShortInfo
from crud.panel import panel_crud
from api.services import get_current_user
from api.validators.user import check_current_user_admin_or_SU
from api.exceptions import forbidden
from models.user import User


router = APIRouter(prefix='/panels', tags=['Панели'])


@router.get(
    '/get_all',
    status_code=status.HTTP_200_OK,
    summary='Получение всех панелей',
    response_model=List[PanelShortInfo]
)
async def get_all_panels(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> List[PanelShortInfo]:
    '''Получение списка всех панелей. Только для админов!'''
    if not await check_current_user_admin_or_SU(user):
        return forbidden(
            'У вас недостаточно прав для получения всех подписок.'
            )
    return await panel_crud.get_all(session=session)


@router.post(
    '/create',
    response_model=PanelShortInfo,
    status_code=status.HTTP_201_CREATED,
    summary='Новая панель',
    dependencies=[Depends(get_current_user)],
)
async def add_panel(
    obj_in: PanelCreate,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> PanelShortInfo:
    """Добавляет в бд новую модель."""
    panel = await panel_crud.create(obj_in=obj_in, session=session)
    return panel


@router.delete(
    '/delete/{panel_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление панели',
)
async def del_panel(
    panel_id: Annotated[int, Path(title='ID панели')],
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    """Удаляет панель из бд. Только для админов."""
    if not await check_current_user_admin_or_SU(user):
        return forbidden(
            'У вас недостаточно прав для получения всех подписок.'
            )
    panel = await panel_crud.get(obj_id=panel_id, session=session)
    if panel:
        await panel_crud.delete(db_obj=panel, session=session)
