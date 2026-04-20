from .base import CRUDBase
from models.panel import Panel
from schemas.panel import PanelCreate, PanelUpdate

from sqlalchemy.ext.asyncio import AsyncSession


class CRUDPanel(CRUDBase[Panel, PanelCreate, PanelUpdate]):
    """CRUD для панели управления."""


panel_crud = CRUDPanel(Panel)
