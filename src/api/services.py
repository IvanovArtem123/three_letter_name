import json
import urllib
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from core.db import get_async_session
from models.user import User
from schemas.user import UserInfo
from models.subscription import Subscription

USER_FIELDS_TO_LOAD = [
    User.id,
    User.username,
    User.uuid,
    User.email,
    User.tg_id,
    User.role,
    User.created_at,
    User.updated_at,
]


async def get_current_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserInfo:
    """Возвращает текущего пользователя по сессии."""
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )

    query = (
        select(User)
        .where(User.id == user_id)
        .options(load_only(*USER_FIELDS_TO_LOAD))
    )
    result = await session.execute(query)
    user = result.scalars().first()

    if user is None:
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return UserInfo.model_validate(user)


async def get_list_inbound_id(data: str) -> list[int]:
    '''Получаем id инбаундов панели.'''
    data = json.loads(data)
    obj = data['obj']
    result = []
    for inbound in obj:
        inbound_id = inbound['id']
        result.append(int(inbound_id))
    return result


async def data_user_config(
        inbound_id: int, user: User, sub: Subscription,
        transport: str
        ) -> dict:
    '''Формируем data для запроса на добавления пользователя в inbound.'''
    if transport == 'xhttp':
        flow = ''
    if transport == 'tcp':
        flow = 'xtls-rprx-vision'
    end_date = sub.end_date
    expiry_time = int(end_date.timestamp() * 1000)
    settings_data = {
        'clients': [
            {
                'id': user.uuid,
                'flow': flow,
                'email': user.email,
                'limitIp': 0,
                'totalGB': 0,
                'expiryTime': expiry_time,
                'enable': True,
                'tgId': user.tg_id,
                'subId': sub.code,
                'comment': user.username,
                'reset': 0
            }
        ]
    }
    data = {
        'id': inbound_id,
        'settings': json.dumps(settings_data)
    }
    return data


async def build_vless_link(
        response_text: str, uuid: str, panel_domain: str) -> str:
    obj = json.loads(response_text)['obj']
    settings = json.loads(obj['settings'])
    stream = json.loads(obj['streamSettings'])
    network = stream.get('network', 'xhttp')
    security = stream.get('security', 'reality')
    transport_key = f"{network}Settings"
    transport = stream.get(transport_key, {})
    params = {}
    params['type'] = network
    params['encryption'] = settings.get('encryption', 'none')
    transport_map = {
        'path': transport.get('path'),
        'host': transport.get('host'),
        'mode': transport.get('mode'),
        'serviceName': transport.get('serviceName'),
        'authority': transport.get('authority'),
        'headerType': transport.get('header', {}).get('type'),
    }
    for k, v in transport_map.items():
        if v:
            params[k] = urllib.parse.quote(str(v), safe='')
    padding = transport.get(
        'xPaddingBytes'
        ) or transport.get(
            'x_padding_bytes')
    if padding:
        params['x_padding_bytes'] = str(padding)
        extra_dict = {"xPaddingBytes": str(padding)}
        sc_max = transport.get('scMaxEachPostBytes')
        if sc_max:
            extra_dict['scMaxEachPostBytes'] = str(sc_max)
        params['extra'] = urllib.parse.quote(
            json.dumps(extra_dict, separators=(',', ':')),
            safe=''
        )
    flow = settings.get('flow', '')
    if flow:
        params['flow'] = flow
    params['security'] = security
    if security == 'reality':
        reality = stream.get('realitySettings', {})
        reality_settings = reality.get('settings', {})
        spx = reality_settings.get('spiderX', '/')
        params['pbk'] = reality_settings.get('publicKey', '')
        params['fp'] = reality_settings.get('fingerprint', 'chrome')
        params['sni'] = (reality.get('serverNames') or [''])[0]
        params['sid'] = (reality.get('shortIds') or [''])[0]
        params['spx'] = urllib.parse.quote(spx, safe='')
    elif security == 'tls':
        tls = stream.get('tlsSettings', {})
        if tls.get('serverName'):
            params['sni'] = tls['serverName']
        if tls.get('fingerprint'):
            params['fp'] = tls['fingerprint']
        if tls.get('alpn'):
            params['alpn'] = urllib.parse.quote(','.join(tls['alpn']), safe='')
    query = '&'.join(f"{k}={v}" for k, v in params.items() if v)
    remark = obj.get('remark', '')
    fragment = urllib.parse.quote(remark) if remark else ''
    vless_url = (f'{obj['protocol']}://{uuid}@' +
                 f'{panel_domain}:{obj['port']}?{query}')
    if fragment:
        vless_url += f"#{fragment}"
    return vless_url


async def get_inbound_transport(
        response_text: str
) -> str:
    '''Получаем транспорт инбаунда.'''
    obj_response = json.loads(response_text)
    obj = json.loads(obj_response['obj']['streamSettings'])
    return obj['network']
