from __future__ import absolute_import
import asyncio
import sports.settings as TSD
from sports.leagues import allLeagues
from sports.request import make_request, send_data_to_api
from sports.sports import sports_for_thesportdb
from sports.teams import leagueTeams
from sports.utils import change_country_name, change_sport_name, check_season


async def transfer_players(session):
    try:
        leagues = await allLeagues(session)
        if leagues['leagues'] is not None:
            sports = await sports_for_thesportdb(session)
            list_sports = [sport['name'] for sport in sports['sports']]
            for league in leagues['leagues']:
                if league['strSport'] in list_sports:
                    teams_in_league = await leagueTeams(session, league['idLeague'])
                    if teams_in_league['teams'] is not None:
                        for team in teams_in_league['teams']:
                            players_for_api = await reformat_players(session, team['idTeam'])
                            if players_for_api:
                                await send_data_to_api(session, 'players', players_for_api)
    except Exception as e:
        # print(f"Players don`t sent. Exception: {e}")
        await asyncio.sleep(5)


async def reformat_players(session, id_team):
    team_players = await teamPlayers(session, id_team)
    if team_players['player'] is not None:
        players_for_api = {'players': []}
        for player in team_players['player']:
            player_contracts = await playersContracts(session, player['idPlayer'])
            player_contracts_for_api = []
            if player_contracts['contracts'] is not None:
                for contract in player_contracts['contracts']:
                    player_contracts_for_api.append({
                        "team": contract["strTeam"],
                        "start_year": contract["strYearStart"],
                        "end_year": contract["strYearEnd"],
                        "wage": contract["strWage"],
                    })
            player_honours = await playersHonours(session, player['idPlayer'])
            player_honours_for_api = []
            if player_honours['honours'] is not None:
                for honour in player_honours['honours']:
                    player_honours_for_api.append({
                        "team": honour["strTeam"],
                        "season": await check_season(honour["strSeason"]),
                        "name": honour["strHonour"],
                    })
            players_for_api['players'].append({
                "country": await change_country_name(player['strNationality']),
                "sport": await change_sport_name(player["strSport"]),
                "team": player["strTeam"],
                "name": player["strPlayer"],
                "date_born": player["dateBorn"],
                "height": player["strHeight"],
                "weight": player["strWeight"],
                "number": player["strNumber"],
                "birth_location": player["strBirthLocation"],
                "description_en": player["strDescriptionEN"],
                "description_ru": player["strDescriptionRU"],
                "gender": player["strGender"],
                "side": player["strSide"],
                "position": player["strPosition"],
                "website": player["strWebsite"],
                "facebook": player["strFacebook"],
                "twitter": player["strTwitter"],
                "instagram": player["strInstagram"],
                "youtube": player["strYoutube"],
                "cutout_large": player["strCutout"],
                "cutout_medium": player["strCutout"] + '/preview' if player["strCutout"] else None,
                "cutout_small": player["strCutout"],
                "thumb_large": player["strThumb"],
                "thumb_medium": player["strThumb"] + '/preview' if player["strThumb"] else None,
                "thumb_small": player["strThumb"] + '/tiny' if player["strThumb"] else None,
                "contracts": player_contracts_for_api,
                "honours": player_honours_for_api
            })
        return players_for_api
    else:
        return None


async def teamPlayers(session, team_id: str):
    return await make_request(session, TSD.TEAM_PLAYERS, id=team_id)


async def playerDetails(session, player_id: str):
    return await make_request(session, TSD.PLAYER, id=player_id)


async def searchPlayersByName(session, player_name: str):
    return await make_request(session, TSD.SEARCH_PLAYERS, p=player_name)


async def playersHonours(session, player_id: str):
    return await make_request(session, TSD.LOOKUP_HONOURS, id=player_id)


async def playersFormerTeam(session, player_id: str):
    return await make_request(session, TSD.LOOKUP_FORMER_TEAMS, id=player_id)


async def playersContracts(session, player_id: str):
    return await make_request(session, TSD.LOOKUP_CONTRACTS, id=player_id)
