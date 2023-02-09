from __future__ import absolute_import
import asyncio
import sports.settings as TSD
import aiohttp


async def _make_url(endpoint: str) -> str:
    return TSD.BASE_URL + TSD.API_KEY + endpoint


async def _make_url_livescore(endpoint: str) -> str:
    return TSD.BASE_URL_V2 + TSD.API_KEY + endpoint


async def make_request(session, endpoint: str, livescore=False, **kwargs):
    params = kwargs
    if livescore:
        URL = await _make_url_livescore(endpoint)
    else:
        URL = await _make_url(endpoint)
    async with session.get(URL, params=params) as response:
        if response.content_type == 'application/json' and response.status == 200:
            return await response.json()
        else:
            return None


async def get_data_from_api(session, endpoint):
    while True:
        try:
            async with session.get(TSD.API_URL + endpoint) as response:
                if response.content_type == 'application/json' and response.status == 200:
                    return await response.json()
        except aiohttp.ClientConnectionError:
            await asyncio.sleep(5)
            continue
        break


async def send_data_to_api(session, endpoint, data_json):
    while True:
        try:
            async with session.post(TSD.API_DATABASE_URL + endpoint, json=data_json) as response:
                if response.content_type == 'application/json' and response.status == 200:
                    await response.json()
        except aiohttp.ClientConnectionError:
            await asyncio.sleep(5)
            continue
        except Exception as e:
            await asyncio.sleep(5)
            continue
        break
