from sports.leagues import get_leagues_ids_by_sports, leagueSeasonTable
from sports.request import send_data_to_api, get_data_from_api
from sports.seasons import allSeason


async def transfer_tables(session):
    sports = await get_data_from_api(session, 'sports')
    leagues_ids = await get_leagues_ids_by_sports(session, sports)
    seasons = [season['name'] for season in await get_data_from_api(session, 'seasons')]
    for id_league in leagues_ids:
        try:
            tables_for_api = await reformat_tables(session, id_league, seasons)
            if tables_for_api:
                await send_data_to_api(session, 'tables', tables_for_api)
        except Exception as e:
            print(f"[TRANSFER_TABLES] Tables don`t sent. Exception: {e}")


async def reformat_tables(session, id_league, seasons):
    thesportsdb_seasons = await allSeason(session, id_league)
    if thesportsdb_seasons['seasons']:
        seasons = sorted([season['strSeason'] for season in thesportsdb_seasons['seasons']
                          if season['strSeason'] in seasons], reverse=True)
    tables_for_api = []
    for season in seasons:
        try:
            table = await leagueSeasonTable(session, id_league, season)
            if table and table['table']:
                for record in table['table']:
                    tables_for_api.append({
                        'team': record['strTeam'],
                        'league': record['strLeague'],
                        'season': season,
                        'rank': record['intRank'],
                        'form': record['strForm'],
                        'description': record['strDescription'],
                        'played': record['intPlayed'],
                        'win': record['intWin'],
                        'draw': record['intDraw'],
                        'loss': record['intLoss'],
                        'goals_for': record['intGoalsFor'],
                        'goals_against': record['intGoalsAgainst'],
                        'goals_difference': record['intGoalDifference'],
                        'points': record['intPoints'],
                        'date_updated': record['dateUpdated']
                    })
        except Exception as e:
            print(f"[REFORMAT_TABLES] Exception: {e}, continue")
            continue
    return tables_for_api
