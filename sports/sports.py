from __future__ import absolute_import
import sports.settings as TSD
from sports.request import make_request, send_data_to_api, get_data_from_api
from sports.utils import change_sport_name, sport_name_for_thesportdb


async def transfer_sports(session):
    try:
        sports = await allSports(session)
        if sports:
            await send_data_to_api(session, 'sports', sports)
    except Exception as e:
        print(f"[TRANSFER_SPORTS] Sports don`t sent. Exception: {e}")


async def allSports(session):
    sports = await make_request(session, TSD.ALL_SPORTS)
    sports_for_api = []
    if sports['sports']:
        for sport in sports['sports']:
            sports_for_api.append({
                'name': await change_sport_name(sport['strSport']),
                'format': sport['strFormat']
            })
        sports_for_api.append({
            'name': 'Olympics',
            'format': 'Any'
        })
    return sports_for_api


async def sports_for_thesportdb(session):
    sports = await get_data_from_api(session, 'sports')
    list_sports = []
    for sport in sports:
        sport['nameEn'] = await sport_name_for_thesportdb(sport['nameEn'])
        list_sports.append(sport['nameEn'])
    return list_sports
