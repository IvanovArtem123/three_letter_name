from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from models.panel import Panel
from crud.panel import panel_crud
from api.exceptions import not_found


async def panels_list_or_404(
    session: AsyncSession
) -> List[Panel]:
    all_panels = await panel_crud.get_all(session)
    if all_panels == []:
        return not_found('Панелей пока не добавлено.')
    return all_panels
