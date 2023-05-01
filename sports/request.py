from __future__ import absolute_import
import asyncio
import sports.settings as TSD
import aiohttp
from sports.utils import check_response


async def _make_url(endpoint: str) -> str:
    return TSD.BASE_URL + TSD.API_KEY + endpoint


async def _make_url_livescore(endpoint: str) -> str:
    return TSD.BASE_URL_V2 + TSD.API_KEY + endpoint


async def send_request(session, url, params):
    while True:
        try:
            async with session.get(url, params=params) as response:
                if response.content_type == 'text/html':
                    break
                if response.content_type == 'application/json' and response.status == 200 \
                        and await check_response(await response.json()):
                    return await response.json()
        except aiohttp.client.ServerDisconnectedError:
            continue


async def make_request(session, endpoint: str, livescore=False, **kwargs):
    params = kwargs
    if livescore:
        url = await _make_url_livescore(endpoint)
    else:
        url = await _make_url(endpoint)
    data = await send_request(session, url, params)
    return data


async def get_data_from_api(session, endpoint):
    while True:
        try:
            async with session.get(TSD.API_URL + endpoint) as response:
                if response.content_type == 'application/json' and response.status == 200:
                    return await response.json()
                await asyncio.sleep(0)
        except aiohttp.ClientConnectionError:
            continue
        break


async def send_data_to_api(session, endpoint, data_json):
    while True:
        try:
            async with session.post(TSD.API_DATABASE_URL + endpoint, json=data_json) as response:
                if response.content_type == 'application/json' and response.status == 200:
                    await response.json()
        except aiohttp.ClientConnectionError:
            continue
        break
