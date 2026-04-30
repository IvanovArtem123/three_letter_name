import requests
import json
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from crud.panel import panel_crud
from crud.subscription import sub_crud
from models.panel import Panel


class GetKeys():
    """Класс получения всех ключей пользователя."""
    def __init__(
            self,
            user_id: int,
            session: AsyncSession
            ):
        self.user_id = user_id
        self.session = session

    async def get_all_panels_by_user_id(self):
        """Получение всех панелей, к которым имеет доступ пользователь."""
        # Получаем все подписки пользователя по его id
        subscription = await sub_crud.get_sub_by_user_id(
            user_id=self.user_id,
            session=self.session
        )
        return subscription.panels

    async def login_panel(self, panel: Panel) -> None:
        """Авторизация на панели управления."""
        # полчаем полную ссылку на панель управления по id панели
        base_url_panel = f"https://{panel.domain}/{panel.path}"
        # авторизация на панели управления и получение токена доступа
        data = {
            'username': panel.login,
            'password': panel.password
        }
        response = requests.post(f"{base_url_panel}/login", json=data)
        if response.status_code == 200:
            cookies_jar = response.cookies
            cookies_dict = requests.utils.dict_from_cookiejar(cookies_jar)
            cookie = json.dumps(cookies_dict)
        # сохраняем cookie в БД для дальнейшего использования
        await panel_crud.update_panel_cookie(
            db_obj=panel,
            cookie=cookie,
            session=self.session
        )

    async def get_user_by_id(self):
        """Получение uuid пользователя по его id."""
        user = await user_crud.get(
            obj_id=self.user_id,
            session=self.session
        )
        return user

    async def get_inbound(self, panel: Panel):
        """Получение inbound панели."""
        inbound_id = 1
        base_url_panel = f"https://{panel.domain}/{panel.path}"
        url_request = base_url_panel + f"/panel/api/inbounds/get/{inbound_id}"
        cookies_jar = await panel_crud.get_cookie_by_panel_id(
            panel_id=panel.id,
            session=self.session
        )
        response = requests.get(url_request, cookies=cookies_jar)
        return response.text

    async def check_auth_cookie(self, panel: Panel) -> bool:
        """Проверка авторизационной cookie панели управления."""
        cookie = await panel_crud.get_cookie_by_panel_id(
            panel_id=panel.id,
            session=self.session)
        base_url_panel = f"https://{panel.domain}/{panel.path}"
        url_request = base_url_panel + "/api/inbounds/list"
        response = requests.get(url_request, cookies=cookie)
        if response.status_code == 200:
            return True
        return False

    async def get_keys(self):
        """Получение всех ключей пользователя."""
        panels = await self.get_all_panels_by_user_id()  # получаем все панели, к которым имеет доступ пользователь
        inbounds = []
        for panel in panels:
            await self.login_panel(panel=panel) # авторизуемся на панели управления и сохраняем cookie в БД
            inbound = await self.get_inbound(panel=panel)
            inbounds.append(inbound)
        return inbounds


class CreateClientInbound():
    """Класс создания клиента в inbound на панели управления."""
    def __init__(
            self,
            user_id: int,
            session: AsyncSession
            ):
        self.user_id = user_id
        self.session = session

    async def add_user_in_inbound(self, inbound_id: int, panels: list[Panel]):
        """Добавление пользователя во все inbound панели."""
        user = await user_crud.get(obj_id=self.user_id, session=self.session)
        sub = await sub_crud.get_sub_by_user_id(
            user_id=self.user_id,
            session=self.session
        )
        expiry_time = int(sub.end_date.timestamp())
        settings_data = {
            'clients': [
                {
                    'id': user.uuid,
                    'flow': '',
                    'email': user.email,
                    'limitIp': 0,
                    'totalGB': 0,
                    'expiryTime': expiry_time,
                    'enable': True,
                    'tgId': user.tg_id,
                    'subId': sub.code,
                    'comment': '',
                    'reset': 0
                }
            ]
        }
        responses = []
        for panel in panels:
            base_url_panel = f"https://{panel.domain}/{panel.path}"
            url_request = base_url_panel + f"/panel/api/inbounds/addClient"
            cookie = await panel_crud.get_cookie_by_panel_id(
                panel_id=panel.id,
                session=self.session
            )
            data = {
                "id": 1,
                "settings": json.dumps(settings_data)
            }
            response = requests.post(
                url_request, 
                data=data,
                cookies=cookie
            )
            responses.append(response.text)
        return responses