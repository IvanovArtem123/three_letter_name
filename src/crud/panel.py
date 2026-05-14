import json

from schemas.panel import PanelCreate, PanelUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.panel import Panel


class CRUDPanel(CRUDBase[Panel, PanelCreate, PanelUpdate]):
    """CRUD для панели управления."""

    async def update_panel_cookie(
        self,
        db_obj: Panel,
        cookie: str,
        session: AsyncSession
    ) -> Panel:
        """Обновить cookie панели управления."""
        db_obj.cookie = cookie
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_cookie_by_panel_id(
        self,
        panel_id: int,
        session: AsyncSession
    ) -> dict | None:
        """Получить cookie панели управления в виде словаря."""
        panel = await self.get(obj_id=panel_id, session=session)
        if not panel or not panel.cookie:
            return None
        if isinstance(panel.cookie, dict):
            return panel.cookie
        if isinstance(panel.cookie, str):
            try:
                return json.loads(panel.cookie)
            except json.JSONDecodeError:
                return None
        return None


panel_crud = CRUDPanel(Panel)
