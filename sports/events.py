from __future__ import absolute_import
import aiohttp
import sports.settings as TSD
from sports.leagues import get_leagues_ids_by_sports
from sports.request import make_request, send_data_to_api, get_data_from_api
from sports.utils import change_country_name, change_sport_name, check_season


async def transfer_events(session):
    sports = await get_data_from_api(session, 'sports')
    leagues_ids = await get_leagues_ids_by_sports(session, sports)
    seasons = await get_data_from_api(session, 'seasons')
    if leagues_ids and seasons:
        for season in seasons:
            for league_id in leagues_ids:
                try:
                    events_for_api = await reformat_events(session, league_id, season['name'])
                    if events_for_api:
                        await send_data_to_api(session, 'events', events_for_api)
                except Exception as e:
                    print(f"[TRANSFER_EVENTS] Events don`t sent. Exception: {e}")
                    continue


async def reformat_events(session, league_id, season_name):
    events = await leagueSeasonEvents(session, league_id, season_name)
    if events and events['events']:
        events_for_api = []
        for event in events['events']:
            try:
                res_event = await generate_event(event, session, season_name)
                events_for_api.append(res_event)
            except Exception as e:
                print(f"[REFORMAT_EVENTS] Exception: {e}, continue")
                continue
        return events_for_api


async def transfer_livescore(sport):
    while True:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3600)) as session:
            livescore_events = await eventLivescore(session, sport)
            if livescore_events and livescore_events['events']:
                events_for_api = []
                for livescore_event in livescore_events['events']:
                    event_info = await eventInfo(session, livescore_event['idEvent'])
                    if event_info and event_info['events']:
                        try:
                            res = await generate_event(
                                event_info['events'][0],
                                session,
                                await check_season(event_info['events'][0]['strSeason'])
                            )
                            events_for_api.append(res)
                        except Exception as e:
                            print(f"[TRANSFER_LIVESCORE] Exception: {e}, continue")
                            continue
                if events_for_api:
                    await send_data_to_api(session, 'events', events_for_api)


async def generate_event(event, session, season_name):
    lineups_for_api = []
    lineups = await eventLineup(session, event['idEvent'])
    if lineups and lineups['lineup']:
        for lineup in lineups['lineup']:
            lineups_for_api.append({
                'team': lineup['strTeam'],
                "player": lineup['strPlayer'],
                "formation": lineup['strFormation'],
                "position": lineup['strPosition'],
                "position_short": lineup['strPositionShort'],
            })
    event_stats_for_api = []
    event_stats = await eventStatistics(session, event['idEvent'])
    if event_stats and event_stats['eventstats']:
        for event_stat in event_stats['eventstats']:
            event_stats_for_api.append({
                "type": event_stat['strStat'],
                "home_team_value": event_stat['intHome'],
                "away_team_value": event_stat['intAway']
            })
    timelines_for_api = []
    timelines = await eventTimeline(session, event['idEvent'])
    if timelines and timelines['timeline']:
        for timeline in timelines['timeline']:
            timelines_for_api.append({
                "team": timeline['strTeam'],
                "name": timeline['strTimeline'],
                "name_detail": timeline['strTimelineDetail'],
                "player": timeline['strPlayer'],
                "player_assist": timeline['strAssist'],
                "minute": timeline['intTime'],
                "comment": timeline['strComment'],
                "date": timeline['dateEvent']
            })
    events_tvs_for_api = []
    events_tvs = await eventTVByEvent(session, event['idEvent'])
    if events_tvs and events_tvs['tvevent']:
        for event_tv in events_tvs['tvevent']:
            events_tvs_for_api.append({
                "date": event_tv['dateEvent'],
                "division": event_tv['intDivision'],
                "timestamp": event_tv['strTimeStamp'] if event_tv['strTimeStamp']
                else event_tv['dateEvent'] + ' ' + event_tv['strTime'],
                "channel": [
                    {
                        "name": event_tv['strChannel'],
                        "logo_large": event_tv['strLogo'],
                        "logo_medium": event_tv['strLogo'],
                        "logo_small": event_tv['strLogo']
                    }
                ]
            })
    res_event = {
        "country": await change_country_name(event['strCountry']),
        "sport": await change_sport_name(event['strSport']),
        "league": event['strLeague'],
        "season": season_name,
        "home_team": event['strHomeTeam'],
        "away_team": event['strAwayTeam'],
        "name": event['strEvent'],
        "name_alt": event['strEventAlternate'],
        "city": event['strCity'],
        "description_en": event['strDescriptionEN'],
        "round": event['intRound'],
        "timestamp": event['strTimestamp'],
        "date": event['dateEvent'],
        "time": event['strTime'],
        "score": event['intScore'],
        "score_votes": event['intScoreVotes'],
        "home_score": event['intHomeScore'],
        "away_score": event['intAwayScore'],
        "result": event['strResult'],
        "venue": event['strVenue'],
        "thumb_large": event['strThumb'],
        "thumb_medium": event['strThumb'] + '/preview' if event['strThumb'] else None,
        "thumb_small": event['strThumb'],
        "banner_large": event['strBanner'],
        "banner_medium": event['strBanner'] + '/preview' if event['strBanner'] else None,
        "banner_small": event['strBanner'],
        "video": event['strVideo'],
        "status": event['strStatus'],
        "is_postponed": event['strPostponed'],
        "lineups": lineups_for_api,
        "event_stats": event_stats_for_api,
        "timelines": timelines_for_api,
        "event_tvs": events_tvs_for_api
    }
    return res_event


async def eventLivescore(session, sport: str):
    return await make_request(session, TSD.EVENT_LIVESCORE, livescore=True, s=sport)


async def eventTVByEvent(session, event_id: str):
    return await make_request(session, TSD.LOOKUP_TV, id=event_id)


async def eventStatistics(session, event_id: str):
    return await make_request(session, TSD.EVENT_STATISTICS, id=event_id)


async def eventLineup(session, event_id: str):
    return await make_request(session, TSD.EVENT_LINEUP, id=event_id)


async def eventTimeline(session, event_id: str):
    return await make_request(session, TSD.EVENT_TIMELINE, id=event_id)


async def leagueSeasonEvents(session, league_id: str, season: str):
    return await make_request(session, TSD.LEAGUE_SEASON_EVENTS, id=league_id, s=season)


async def eventInfo(session, event_id: str):
    return await make_request(session, TSD.EVENT, id=event_id)
