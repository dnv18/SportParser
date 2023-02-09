from __future__ import absolute_import
import asyncio
import sports.settings as TSD
from sports.request import make_request, send_data_to_api
from sports.seasons import allSeason
from sports.utils import check_season, change_sport_name, change_country_name


async def transfer_leagues(session):
    try:
        leagues = await allLeagues(session)
        leagues_for_api = await reformat_leagues(session, leagues)
        if leagues_for_api:
            await send_data_to_api(session, 'leagues', leagues_for_api)
    except Exception as e:
        # print(f"Leagues don`t sent. Exception: {e}")
        await asyncio.sleep(5)


async def get_leagues_ids_by_sports(session, sports):
    leagues = await allLeagues(session)
    leagues_ids = []
    for league in leagues['leagues']:
        for sport in sports['sports']:
            if await change_sport_name(league['strSport']) == sport['name']:
                leagues_ids.append(league['idLeague'])
    return leagues_ids


async def reformat_leagues(session, leagues):
    leagues_for_api = {'leagues': []}
    try:
        for league in leagues['leagues']:
            try:
                league_info = await leagueInfo(session, league['idLeague'])
                if league_info is not None:
                    for i in league_info['leagues']:
                        league_seasons = await allSeason(session, i['idLeague'])
                        seasons_for_api = []
                        if league_seasons['seasons'] is not None:
                            for league_season in league_seasons['seasons']:
                                seasons_for_api.append({
                                    'name': await check_season(league_season['strSeason'])
                                })
                        leagues_for_api['leagues'].append({
                            'sport': await change_sport_name(i['strSport']),
                            'country': await change_country_name(i['strCountry']),
                            'id_cup': i['idCup'],
                            'name': i['strLeague'],
                            'name_alt': i['strLeagueAlternate'],
                            'division': i['intDivision'],
                            'formed_year': i['intFormedYear'],
                            'date_first_event': i['dateFirstEvent'],
                            'gender': i['strGender'],
                            'website': i['strWebsite'],
                            'facebook': i['strFacebook'],
                            'twitter': i['strTwitter'],
                            'instagram': i['strInstagram'],
                            'youtube': i['strYoutube'],
                            'rss': i['strRSS'],
                            'description_en': i['strDescriptionEN'],
                            'description_ru': i['strDescriptionRU'],
                            'tv_rights': i['strTvRights'],
                            'logo_large': i["strBadge"],
                            'logo_medium': i["strBadge"] + '/preview' if i['strBadge'] else None,
                            'logo_small': i["strBadge"] + '/tiny' if i['strBadge'] else None,
                            'trophy': i['strTrophy'],
                            'seasons': seasons_for_api
                        })
            except Exception as e:
                # print(f"Leagues info not found by league id: {league['idLeague']}. Error: {e}")
                continue
    except TypeError:
        pass
    return leagues_for_api


async def allLeagues(session):
    return await make_request(session, TSD.ALL_LEAGUES)


async def leagueSeasonTable(session, league_id: str, season: str):
    return await make_request(session, TSD.LEAGUE_SEASON_TABLE, l=league_id, s=season)


async def leagueInfo(session, league_id: str):
    return await make_request(session, TSD.LEAGUE, id=league_id)
