from __future__ import absolute_import
import asyncio
import sports.settings as TSD
from sports.leagues import allLeagues
from sports.request import make_request, send_data_to_api
from sports.utils import change_sport_name, change_country_name


async def transfer_teams(session):
    try:
        leagues = await allLeagues(session)
        for league in leagues['leagues']:
            teams_for_api = await reformat_teams(session, league['idLeague'])
            if teams_for_api:
                await send_data_to_api(session, 'teams', teams_for_api)
    except Exception as e:
        # print(f"Teams don`t sent. Exception: {e}")
        await asyncio.sleep(5)


async def reformat_teams(session, id_league):
    teams_in_league = await leagueTeams(session, id_league)
    if teams_in_league['teams'] is not None:
        teams_for_api = {'teams': []}
        for team in teams_in_league['teams']:
            teams_for_api['teams'].append({
                "country": await change_country_name(team['strCountry']),
                "sport": await change_sport_name(team['strSport']),
                "league": team['strLeague'],
                "name": team['strTeam'],
                "name_alt": team['strAlternate'],
                "name_short": team['strTeamShort'],
                "formed_year": team['intFormedYear'],
                "gender": team['strGender'],
                "division": team['strDivision'],
                "manager": team['strManager'],
                "keywords": team['strKeywords'],
                "website": team['strWebsite'],
                "facebook": team['strFacebook'],
                "twitter": team['strTwitter'],
                "instagram": team['strInstagram'],
                "youtube": team['strYoutube'],
                "rss": team['strRSS'],
                "description_en": team['strDescriptionEN'],
                "description_ru": team['strDescriptionRU'],
                "logo_large": team['strTeamBadge'],
                "logo_medium": team['strTeamBadge'] + '/preview' if team['strTeamBadge'] else None,
                "logo_small": team['strTeamBadge'] + '/tiny' if team['strTeamBadge'] else None,
                "stadium": [
                    {
                        "name": team['strStadium'],
                        "capacity": team['intStadiumCapacity'],
                        "location": team['strStadiumLocation'],
                        "description": team['strStadiumDescription'],
                        "thumb": team['strStadiumThumb']
                    }
                ]
            })
        return teams_for_api
    else:
        return None


async def leagueTeams(session, league_id: str):
    return await make_request(session, TSD.LEAGUE_TEAMS, id=league_id)


async def teamInfo(session, team_id: str):
    return await make_request(session, TSD.TEAM, id=team_id)


async def searchTeamsByName(session, team_name: str):
    return await make_request(session, TSD.SEARCH_TEAMS, t=team_name)


async def equipment(session, team_id: str):
    return await make_request(session, TSD.LOOKUP_EQUIPMENT, id=team_id)
