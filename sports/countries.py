from __future__ import absolute_import
import asyncio
import sports.settings as TSD
from sports.request import make_request, send_data_to_api


async def transfer_countries(session):
    try:
        countries = await allCountries(session)
        if countries:
            await send_data_to_api(session, 'countries', countries)
    except Exception as e:
        # print(f"Countries don`t sent. Exception: {e}")
        await asyncio.sleep(5)


async def allCountries(session):
    countries = await make_request(session, TSD.ALL_COUNTRIES)
    countries['countries'].append({
        'name_en': 'Netherlands'
    })
    return countries
