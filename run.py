import asyncio
from datetime import datetime
import aiohttp
import aioschedule
from sports.countries import transfer_countries
from sports.events import transfer_events, transfer_livescore
from sports.leagues import transfer_leagues
from sports.players import transfer_players
from sports.sports import transfer_sports, sports_for_thesportdb
from sports.teams import transfer_teams


async def main():
    start_mode = input('Choose start mode: 1 - First start, 2 - Restart\n')
    async with aiohttp.ClientSession() as session:
        match start_mode:
            case '1':
                b = datetime.now()
                await transfer_sports(session)
                await transfer_countries(session)
                await transfer_leagues(session)
                await transfer_teams(session)
                await transfer_players(session)
                await transfer_events(session)
                print(datetime.now() - b)
                await run_aioschedule(session)
            case '2':
                await run_aioschedule(session)
            case _:
                print("Wrong choose")


async def run_aioschedule(session):
    aioschedule.every().day.do(lambda: transfer_countries(session))
    aioschedule.every().day.do(lambda: transfer_sports(session))
    aioschedule.every().day.do(lambda: transfer_leagues(session))
    aioschedule.every().day.do(lambda: transfer_teams(session))
    aioschedule.every().day.do(lambda: transfer_players(session))
    aioschedule.every().day.do(lambda: transfer_events(session))
    sports = await sports_for_thesportdb(session)
    aioschedule.every(1).seconds.do(lambda: transfer_livescore(session, sports[0]))
    aioschedule.every(15).seconds.do(lambda: transfer_livescore(session, sports[1]))
    aioschedule.every(15).seconds.do(lambda: transfer_livescore(session, sports[2]))
    aioschedule.every(1).seconds.do(lambda: transfer_livescore(session, sports[3]))
    while True:
        await aioschedule.run_pending()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Close application.")
