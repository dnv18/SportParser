from __future__ import absolute_import
import sports.settings as TSD
from sports.request import make_request, send_data_to_api


async def transfer_countries(session):
    try:
        countries = await allCountries(session)
        if countries:
            await send_data_to_api(session, 'countries', countries)
    except Exception as e:
        print(f"[TRANSFER_COUNTRIES] Countries don`t sent. Exception: {e}")


async def allCountries(session):
    countries = await make_request(session, TSD.ALL_COUNTRIES)
    if countries['countries']:
        countries['countries'].append({
            'name_en': 'Netherlands'
        })
    return countries['countries']
