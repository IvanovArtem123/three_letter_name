from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models.panel import Panel
from crud.panel import panel_crud
from api.exceptions import not_found


async def panels_list_or_404(
    session: AsyncSession
) -> List[Panel]:
    '''Возвращаем список панелей или ошибку 404.'''
    all_panels = await panel_crud.get_all(session)
    if all_panels == []:
        return not_found('Панелей пока не добавлено.')
    return all_panels


async def get_panel_or_404(
    panel_id: int,
    session: AsyncSession
) -> Panel:
    '''Получаем панель или возвращаем ошибку 404.'''
    panel = await panel_crud.get(obj_id=panel_id, session=session)
    if panel is None:
        return not_found('Панели не найдено.')
    return panel
