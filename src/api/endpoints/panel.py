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
    panel = await panel_crud.create(obj_in=obj_in, session=session)
    return panel
