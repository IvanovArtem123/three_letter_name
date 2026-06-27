import base64
import json
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
from core.db import get_async_session


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

    async def get_keys(self) -> str:
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


class ManageUserUI():
    ''''Класс управления пользовательскими функциями панели.'''

    def __init__(
            self, panels_list: list[Panel], user: User, session: AsyncSession,
            sub: Subscription):
        self.panels_list = panels_list
        self.user = user
        self.headers = {'Authorization': f'Bearer {TOKEN_PANEL}'}
        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20)
        )
        self.session = session
        self.sub = sub

    async def _get_list_inbounds(self, base_url_panel: str):
        '''Получение списка inbound панели управления.'''
        url = (f'{base_url_panel}/panel/api/inbounds/list')
        try:
            response = await self.client.get(url=url, headers=self.headers)
            return json.loads(response.text)
        except httpx.HTTPError as e:
            return f"Ошибка при получении списка inbounds: {e}"

    async def _get_inbound_info(self, inbound_id: int, base_url_panel: str):
        '''Получение информации об Inbound.'''
        url = (f'{base_url_panel}/panel/api/inbounds/get/{inbound_id}')
        try:
            response = await self.client.get(url=url, headers=self.headers)
            return json.loads(response.text)
        except httpx.HTTPError as e:
            return f"Ошибка при получении информации об Inbound: {e}"

    async def _add_inbound(self):
        '''Добавление Inbound.'''

    async def _del_inbound_by_id(self):
        '''Удаление Inbound по id.'''

    async def _get_list_clients(self):
        '''Получение списка клиентов инбаунда.'''

    async def _del_client_by_mail(self):
        '''Удаление клиента по почте.'''

    async def _add_client(self, inbound_ids: list[int], base_url_panel: str):
        '''Добавление клиента.'''
        url = (f'{base_url_panel}/panel/api/clients/add')
        data = {
            "client": {
                "email": self.user.email,
                "totalGB": 0,
                "expiryTime": int(self.sub.end_date.timestamp() * 1000),
                "tgId": self.user.tg_id,
                "limitIp": 0,
                "enable": True
            },
            "inboundIds": inbound_ids
            }
        try:
            response = await self.client.post(
                url=url, headers=self.headers, json=data)
            return json.loads(response.text)
        except httpx.HTTPError as e:
            return f"Ошибка при добавлении клиента: {e}"

    async def _get_keys_user_in_panel(
            self, base_url_panel: str) -> list[str] | str:
        '''Получение всех ключей для подписки.'''
        url = (base_url_panel + f'/panel/api/clients/links/{self.user.email}')
        try:
            response = await self.client.get(url=url, headers=self.headers)
            keys = response.json().get('obj')
            return keys
        except httpx.HTTPError as e:
            return f"Ошибка при получении ключей: {e}"

    async def add_client_to_inbounds(self) -> None:
        '''Добавление клиента во все inbound панели управления.'''
        for panel in self.panels_list:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            inbounds = await self._get_list_inbounds(base_url_panel=base_url_panel)  # Получаем список инбаундов
            inbound_ids = [inbound['id'] for inbound in inbounds['obj']]  # Извлекаем id инбаундов
            await self._add_client(inbound_ids=inbound_ids, base_url_panel=base_url_panel)  # Добавляем пользователя в данные инбаунды панели

    async def get_keys(self) -> str:
        '''Получение всех ключей для подписки.'''
        all_keys = []
        for panel in self.panels_list:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            keys_panel = await self._get_keys_user_in_panel(
                base_url_panel=base_url_panel)
            if keys_panel is not None:
                all_keys.extend(keys_panel)
        return all_keys

    async def delete_client_by_subid(self) -> None:
        '''Удаление всех клиентов для полученных inbounds.'''
        panels = self.sub.panels
        for panel in panels:
            base_url_panel = f"https://{panel.domain}{panel.port}/{panel.path}"
            url = (base_url_panel + '/panel/api/clients/del/{email}')
            await self.client.post(url=url, headers=self.headers)
