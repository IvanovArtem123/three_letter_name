import json
from typing import List

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from models.panel import Panel
from models.user import User
from models.subscription import Subscription
from core.constants import TOKEN_PANEL


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
            return f'Ошибка при получении списка inbounds: {e}'

    async def _get_inbound_info(self, inbound_id: int, base_url_panel: str):
        '''Получение информации об Inbound.'''
        url = (f'{base_url_panel}/panel/api/inbounds/get/{inbound_id}')
        try:
            response = await self.client.get(url=url, headers=self.headers)
            return json.loads(response.text)
        except httpx.HTTPError as e:
            return f'Ошибка при получении информации об Inbound: {e}'

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
            'client': {
                'email': self.user.email,
                'totalGB': 0,
                'expiryTime': int(self.sub.end_date.timestamp() * 1000),
                'tgId': self.user.tg_id,
                'limitIp': 0,
                'subId': self.sub.code,
                'flow': 'xtls-rprx-vision',
                'enable': True
            },
            'inboundIds': inbound_ids
            }
        try:
            response = await self.client.post(
                url=url, headers=self.headers, json=data)
            return json.loads(response.text)
        except httpx.HTTPError as e:
            return f'Ошибка при добавлении клиента: {e}'

    async def _get_keys_user_in_panel(
            self, base_url_panel: str) -> list[str] | str:
        '''Получение всех ключей для подписки.'''
        url = (base_url_panel + f'/panel/api/clients/links/{self.user.email}')
        try:
            response = await self.client.get(url=url, headers=self.headers)
            keys = response.json().get('obj')
            return keys
        except httpx.HTTPError as e:
            return f'Ошибка при получении ключей: {e}'

    async def add_client_to_inbounds(self) -> None:
        '''Добавление клиента во все inbound панели управления.'''
        for panel in self.panels_list:
            base_url_panel = f'https://{panel.domain}{panel.port}/{panel.path}'
            inbounds = await self._get_list_inbounds(
                base_url_panel=base_url_panel)  # Получаем список инбаундов
            inbound_ids = [inbound['id'] for inbound in inbounds['obj']]
            await self._add_client(
                inbound_ids=inbound_ids, base_url_panel=base_url_panel)

    async def get_keys(self) -> list[str | None]:
        '''Получение всех ключей для подписки.'''
        all_keys: List[str | None] = []
        for panel in self.panels_list:
            base_url_panel = f'https://{panel.domain}{panel.port}/{panel.path}'
            keys_panel = await self._get_keys_user_in_panel(
                base_url_panel=base_url_panel)
            if keys_panel is not None:
                all_keys.extend(keys_panel)
        return all_keys

    async def delete_client_by_subid(self) -> None:
        '''Удаление всех клиентов для полученных inbounds.'''
        panels = self.sub.panels
        for panel in panels:
            base_url_panel = f'https://{panel.domain}{panel.port}/{panel.path}'
            url = (base_url_panel + '/panel/api/clients/del/{email}')
            await self.client.post(url=url, headers=self.headers)
