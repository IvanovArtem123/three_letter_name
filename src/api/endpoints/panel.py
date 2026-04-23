from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from schemas.panel import PanelCreate, PanelShortInfo
from crud.panel import panel_crud
from api.services import get_current_user


router = APIRouter(prefix='/panels', tags=['Панели'])

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
    panel = await panel_crud.create_be_hash_pass(obj_in=obj_in, session=session)
    return panel

@router.delete(
    '/delete/{panel_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление панели',
)
async def panel(
    panel_id: Annotated[int, Path(title='ID панели')],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> None:
    """Удаляет панель из бд."""
    panel = await panel_crud.get(obj_id=panel_id, session=session)
    if panel:
        await panel_crud.delete(db_obj=panel, session=session)