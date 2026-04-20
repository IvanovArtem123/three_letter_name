from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from schemas.panel import PanelCreate, PanelShortInfo
from crud.panel import panel_crud


router = APIRouter(prefix='/panels', tags=['Панели'])

@router.post(
    '/',
    response_model=PanelShortInfo,
    status_code=status.HTTP_200_OK,
    summary='Новая панель',
)
async def create_action(
    obj_in: PanelCreate,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> PanelShortInfo:
    """Добавляет в бд новую модель."""
    panel = await panel_crud.create_be_hash_pass(obj_in=obj_in, session=session)
    return panel

@router.delete(
    '/{panel_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Новая панель',
)
async def delete_action(
    panel_id: Annotated[int, Path(title='ID панели')],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> None:
    """Удаляет панель из бд."""
    panel = await panel_crud.get(obj_id=panel_id, session=session)
    if panel:
        await panel_crud.delete(db_obj=panel, session=session)
