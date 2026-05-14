import base64
from typing import Dict, Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from crud.panel import panel_crud
from models.panel import Panel
from models.user import User
from models.subscription import Subscription
from api.services import (
    get_list_inbound_id, data_user_config, build_vless_link,
    get_inbound_transport
)
from core.constants import TOKEN_PANEL


class AddUserToInbounds():
    """Класс добавления пользователя во все inbound панели управления."""
    def __init__(
            self,
            user: User,
            sub: Subscription,
            session: AsyncSession,
            ):
        self.user = user
        self.sub = sub
        self.session = session
        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20)
        )
        self.headers = {'Authorization': f'Bearer {TOKEN_PANEL}'}

    async def _check_auth_cookie(
         self, panel: Panel, base_url_panel: str
    ) -> bool:
        """Проверка авторизационной cookie панели управления."""
        cookie = await panel_crud.get_cookie_by_panel_id(
            panel_id=panel.id,
            session=self.session)
        url = base_url_panel + "/api/inbounds/list"
        response = await self.client.get(url=url, cookies=cookie, timeout=30)
        if response.status_code != 200:
            return False
        return True

    async def _login_panel(
        self, panel: Panel, base_url_panel: str
    ) -> Dict[str, Any]:
        """Авторизация на панели управления. Возврат cookie как словаря."""
        data = {
            'username': panel.login,
            'password': panel.password
        }
        response = await self.client.post(
            url=f"{base_url_panel}/login",
            json=data
        )
        if response.status_code == 200:
            cookies_dict = dict(response.cookies)
        else:
            raise Exception(f"Login failed with status {response.status_code}")
        new_panel = await panel_crud.update_panel_cookie(
            db_obj=panel,
            cookie=cookies_dict,
            session=self.session
        )
        return new_panel.cookie

    async def _get_inbounds(
            self, base_url_panel: str) -> list[int]:
        """Получение списка inbound панели управления."""
        url = base_url_panel + "/panel/api/inbounds/list"
        response = await self.client.get(url=url, headers=self.headers)
        data = response.text
        return await get_list_inbound_id(data)

    async def _add_client_to_inbound(
        self, base_url_panel: str, inbound_id: int
    ) -> int:
        '''Добавляем клиента в инбаунд. Возвращаем код ответа.'''
        url = base_url_panel + '/panel/api/inbounds/addClient'
        user = self.user
        sub = self.sub
        inbound = await self._get_inbound(inbound_id=inbound_id,
                                          base_url_panel=base_url_panel)
        data = await data_user_config(
            inbound_id=inbound_id,
            user=user,
            sub=sub,
            transport=await get_inbound_transport(inbound)
            )
        response = await self.client.post(
            url=url, headers=self.headers, json=data)
        return response.status_code

    async def _get_inbound(
            self, inbound_id: int, base_url_panel: str
    ) -> str:
        '''Получение информации об Inbound.'''
        url = base_url_panel + f'/panel/api/inbounds/get/{inbound_id}'
        response = await self.client.get(url=url, headers=self.headers)
        return response.text

    async def _del_client(
            self, inbound_id: int, uuid: str, base_url_panel: str
    ) -> int:
        url = (base_url_panel +
               f'/panel/api/inbounds/{inbound_id}/delClient/{uuid}')
        response = await self.client.post(url=url, headers=self.headers)
        return response.status_code

    async def add_user_to_inbounds(self) -> list[str]:
        """Добавление пользователя во все inbound панели управления."""
        panels = self.sub.panels
        result = []
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            inbounds_id = await self._get_inbounds(
                base_url_panel=base_url_panel)
            for inbound_id in inbounds_id:

                status_code = await self._add_client_to_inbound(
                    base_url_panel=base_url_panel,
                    inbound_id=inbound_id
                )
                result.append(str(status_code))
        return result

    async def get_keys_to_subscriprion(self) -> list[str]:
        '''Получение всех ключей для подписки.'''
        keys = []
        uuid = self.user.uuid
        panels = self.sub.panels
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            inbounds_id = await self._get_inbounds(
                base_url_panel=base_url_panel)
            for inbound_id in inbounds_id:
                panel_domain = panel.domain.split(':')[0]
                inbound_text = await self._get_inbound(
                    base_url_panel=base_url_panel,
                    inbound_id=inbound_id
                )
                key = await build_vless_link(
                    response_text=inbound_text,
                    uuid=uuid,
                    panel_domain=panel_domain
                )
                keys.append(key)
        return keys

    async def delete_client(self) -> None:
        '''Удаление всех клиентов для полученных inbounds.'''
        uuid = self.user.uuid
        panels = self.sub.panels
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            inbounds_id = await self._get_inbounds(
                base_url_panel=base_url_panel)
            for inbound_id in inbounds_id:
                await self._del_client(
                    inbound_id=inbound_id, uuid=uuid,
                    base_url_panel=base_url_panel)

    async def get_keys_by_subid(self) -> str:
        '''Получение всех ключей для подписки.'''
        panels = self.sub.panels
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
        url = (base_url_panel + '/panel/api/inbounds/' +
               f'getSubLinks/{self.sub.code}')
        response = await self.client.get(url=url, headers=self.headers)
        keys = response.json().get('obj')
        keys_str = '\n'.join(keys)
        encoded = base64.b64encode(keys_str.encode('utf-8')).decode('utf-8')
        return encoded

    async def delete_client_by_subid(self) -> None:
        '''Удаление всех клиентов для полученных inbounds.'''
        panels = self.sub.panels
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            inbounds_id = await self._get_inbounds(
                base_url_panel=base_url_panel)
        for inbound_id in inbounds_id:
            url = (base_url_panel + '/panel/api/inbounds/' +
                   f'{inbound_id}/delClient/{self.user.uuid}')
            await self.client.post(url=url, headers=self.headers)
