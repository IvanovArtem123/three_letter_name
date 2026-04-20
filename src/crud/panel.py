from schemas.panel import PanelCreate, PanelUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.panel import Panel
from core.security import hash_password


class CRUDPanel(CRUDBase[Panel, PanelCreate, PanelUpdate]):
    """CRUD для панели управления."""

    async def create_be_hash_pass(
        self,
        obj_in: PanelCreate,
        session: AsyncSession
    ):
        """Создание панели управления с хешированием пароля."""
        obj_panel = Panel(
            path = obj_in.path,
            domain = obj_in.domain,
            login = obj_in.login,
            password_hash = await hash_password(obj_in.password),
            country = obj_in.country
        )
        session.add(obj_panel)
        await session.commit()
        await session.refresh(obj_panel)
        return obj_panel


panel_crud = CRUDPanel(Panel)
