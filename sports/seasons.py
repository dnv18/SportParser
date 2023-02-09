from __future__ import absolute_import
import sports.settings as TSD
from sports.request import make_request


async def allSeason(session, league_id: str):
    return await make_request(session, TSD.SEASONS, id=league_id)
