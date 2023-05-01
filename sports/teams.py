from __future__ import absolute_import
import sports.settings as TSD
from sports.leagues import allLeagues, leagueInfo
from sports.request import make_request, send_data_to_api
from sports.sports import sports_for_thesportdb
from sports.utils import change_sport_name, change_country_name


async def transfer_teams(session):
    try:
        sports = await sports_for_thesportdb(session)
        leagues = await allLeagues(session)
        if leagues['leagues'] and sports:
            for league in leagues['leagues']:
                if league['strSport'] in sports:
                    teams_for_api = await reformat_teams(session, league['idLeague'])
                    if teams_for_api:
                        await send_data_to_api(session, 'teams', teams_for_api)
    except Exception as e:
        print(f"[TRANSFER_TEAMS] Teams don`t sent. Exception: {e}")


async def reformat_teams(session, id_league):
    teams_in_league = await leagueTeams(session, id_league)
    league_info = await leagueInfo(session, id_league)
    if teams_in_league['teams'] and league_info['leagues']:
        teams_for_api = []
        for team in teams_in_league['teams']:
            try:
                stadium = {
                    "name": team['strStadium'],
                    "capacity": team['intStadiumCapacity'],
                    "location": team['strStadiumLocation'],
                    "description": team['strStadiumDescription'],
                    "thumb": team['strStadiumThumb']
                }
                teams_for_api.append({
                    "country": await change_country_name(team['strCountry']),
                    "sport": await change_sport_name(team['strSport']),
                    "league": league_info['leagues'][0]['strLeague'],
                    "name": team['strTeam'],
                    "name_alt": team['strAlternate'],
                    "name_short": team['strTeamShort'],
                    "formed_year": team['intFormedYear'],
                    "gender": team['strGender'],
                    "division": team['strDivision'],
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
                    "stadium": [stadium] if stadium['name'] else None
                })
            except Exception as e:
                print(f"[REFORMAT_TEAMS] Exception: {e}, continue")
                continue
        return teams_for_api


async def leagueTeams(session, id_league: str):
    return await make_request(session, TSD.LEAGUE_TEAMS, id=id_league)


async def teamInfo(session, team_id: str):
    return await make_request(session, TSD.TEAM, id=team_id)


async def searchTeamsByName(session, team_name: str):
    return await make_request(session, TSD.SEARCH_TEAMS, t=team_name)


async def equipment(session, team_id: str):
    return await make_request(session, TSD.LOOKUP_EQUIPMENT, id=team_id)
