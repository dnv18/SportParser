from __future__ import absolute_import
import asyncio
import sports.settings as TSD
from sports.request import make_request, send_data_to_api, get_data_from_api
from sports.utils import change_sport_name, sport_name_for_thesportdb


async def transfer_sports(session):
    try:
        sports_for_api = await allSports(session)
        if sports_for_api:
            await send_data_to_api(session, 'sports', sports_for_api)
    except Exception as e:
        # print(f"Sports don`t sent. Exception: {e}")
        await asyncio.sleep(5)


async def allSports(session):
    sports = await make_request(session, TSD.ALL_SPORTS)
    sports_for_api = {'sports': []}
    for sport in sports['sports']:
        sports_for_api['sports'].append({
            'name': await change_sport_name(sport['strSport']),
            'format': sport['strFormat']
        })
    sports_for_api['sports'].append({
        'name': 'Olympics',
        'format': 'Any'
    })
    return sports_for_api


async def sports_for_thesportdb(session):
    sports = await get_data_from_api(session, 'sports')
    for sport in sports['sports']:
        sport['name'] = await sport_name_for_thesportdb(sport['name'])
    return sports
