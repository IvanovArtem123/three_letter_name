from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Body


from core.db import get_async_session
from schemas.panel import PanelCreate, PanelInfo, PanelShortInfo, PanelUpdate
from crud.panel import panel_crud
from api.services import get_current_user
from api.validators.user import check_current_user_admin
from api.validators.panel import get_panel_or_404
from api.exceptions import forbidden
from models.user import User
from core.constants import (
    EXAMPLE_PATH_PANEL,
    EXAMPLE_DOMAIN_PANEL,
    EXAMPLE_PORT_PANEL
)


router = APIRouter(prefix='/panels', tags=['Панели'])


@router.get(
    '/get/{panel_id}',
    status_code=status.HTTP_200_OK,
    summary='Получение информации о панели',
    response_model=PanelInfo
)
async def get_panel(
    user: Annotated[User, Depends(get_current_user)],
    panel_id: Annotated[int, Path(title='ID панели')],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> PanelInfo:
    '''Получение информации о панели.'''
    if not await check_current_user_admin(user):
        return forbidden(
            'У вас недостаточно прав для получения информации о панели.'
            )
    panel = await get_panel_or_404(panel_id=panel_id, session=session)
    return panel


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
    if not await check_current_user_admin(user):
        return forbidden(
            'У вас недостаточно прав для получения информации о панелях.'
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
    session: Annotated[AsyncSession, Depends(get_async_session)],
    obj_in: PanelCreate = Body(
                openapi_examples={
                    'Panel1': {
                        'summary': 'Пример панели',
                        'value': {
                            'path': EXAMPLE_PATH_PANEL,
                            'domain': EXAMPLE_DOMAIN_PANEL,
                            'port': EXAMPLE_PORT_PANEL,
                            'country': 'Германия'
                        }
                    }
                }
            )
) -> PanelShortInfo:
    """Добавляет в бд новую модель."""
    panel = await panel_crud.create(obj_in=obj_in, session=session)
    return panel


@router.patch(
    '/update/{panel_id}',
    response_model=PanelShortInfo,
    summary='Обновление панели'
)
async def update_panel(
    user: Annotated[User, Depends(get_current_user)],
    panel_id: Annotated[int, Path(title='ID панели')],
    panel_in: PanelUpdate,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> PanelShortInfo:
    '''Обновление панели.'''
    if not check_current_user_admin(user=user):
        return forbidden('Недостаточно прав для изменения данных панели.')
    panel = await get_panel_or_404(panel_id=panel_id, session=session)
    update_panel = await panel_crud.update(
        db_obj=panel, obj_in=panel_in, session=session)
    return update_panel


@router.delete(
    '/delete/{panel_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление панели',
)
async def del_panel(
    user: Annotated[User, Depends(get_current_user)],
    panel_id: Annotated[int, Path(title='ID панели')],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    """Удаляет панель из бд. Только для админов."""
    if not await check_current_user_admin(user):
        return forbidden('У вас недостаточно прав для удаления панели.')
    panel = await panel_crud.get(obj_id=panel_id, session=session)
    if panel:
        await panel_crud.delete(db_obj=panel, session=session)
