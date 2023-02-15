import re


async def change_sport_name(str_sport):
    match str_sport:
        case 'Soccer':
            return 'Football'
        case 'Ice Hockey':
            return 'Hockey'
        case 'Esports':
            return 'ESports'
        case 'MotorSport':
            return 'Motorsport'
        case _:
            return str_sport


async def sport_name_for_thesportdb(str_sport):
    match str_sport:
        case 'Football':
            return 'Soccer'
        case 'Hockey':
            return 'Ice Hockey'
        case 'ESports':
            return 'Esports'
        case 'Motorsport':
            return 'MotorSport'
        case _:
            return str_sport


async def change_country_name(str_country):
    match str_country:
        case 'World':
            return 'Worldwide'
        case 'USA':
            return 'United States'
        case 'Bosnia':
            return 'Bosnia and Herzegovina'
        case 'UAE':
            return 'United Arab Emirates'
        case 'Russia':
            return 'Russian Federation'
        case 'Laos':
            return "Lao People's Democratic Republic"
        case 'Ivory Coast':
            return "Côte d'Ivoire"
        case 'Palestine':
            return 'Palestine, State of'
        case _:
            return str_country


async def check_season(season: str):
    season_elements = re.sub('^\s+|\n|\r|\s+$', '', season).split('-')
    if len(season_elements) > 1:
        if season_elements[0] > season_elements[1]:
            return season_elements[1] + '-' + season_elements[0]
        else:
            return season_elements[0] + '-' + season_elements[1]
    else:
        return season_elements[0]
