import requests, pandas, time, random
from bs4 import BeautifulSoup
from .teams import _tms


def _standardized_with_side(
    tm_or_opp,
    reference_team,
):

    tms = _tms()

    tm_tags = (
        'nano',
        'market',
        'name',
        'alias',
    )

    standardized = {
        f'{tm_or_opp}_{tm_tag}': tms.get(
            reference_team.lower(),
        ).get(
            tm_tag
        )
        for tm_tag in tm_tags
    }

    return standardized


def _is_playoff_filler(
    gamelog,
):
    event_date_text = gamelog.find(
        attrs={'data-stat': 'game_date'}
    ).text
    
    if event_date_text == 'Playoffs':
        return False
    else:
        return True


def _week(
    season,
    gamelog, 
):
    week_text = gamelog.find(
        attrs={
            'data-stat': 'week_num'
        }
    ).text

    week = None

    if 1970 <= season <= 1977:
        if week_text == "Division":
            week = 15
        elif week_text == "ConfChamp":
            week = 16
        elif week_text == "SuperBowl":
            week = 17
        else:
            week = int(week_text)  
    
    if 1978 <= season <= 1989:
        if week_text == "WildCard":
            week = 17
        elif week_text == "Division":
            week = 18
        elif week_text == "ConfChamp":
            week = 19
        elif week_text == "SuperBowl":
            week = 20
        else:
            week = int(week_text)  
    
    if 1990 <= season <= 2020:
        if week_text == "WildCard":
            week = 18
        elif week_text == "Division":
            week = 19
        elif week_text == "ConfChamp":
            week = 20
        elif week_text == "SuperBowl":
            week = 21
        else:
            week = int(week_text)

    if 2021 <= season:
        if week_text == "WildCard":
            week = 19
        elif week_text == "Division":
            week = 20
        elif week_text == "ConfChamp":
            week = 21
        elif week_text == "SuperBowl":
            week = 22
        else:
            week = int(week_text)

    return {
        'week': week
    }


def _week_day(
    gamelog,
):
    week_day = gamelog.find(
        attrs={'data-stat': 'game_day_of_week'}
    ).text
    
    return {
        'week_day': week_day
    }


def _event_date(
    gamelog,
):
    event_date = gamelog.find(
        attrs={'data-stat': 'game_date'}
    ).text

    return {
        'event_date': event_date
    }


def _alt_alias_and_market(
    tm_or_opp,
    side,
    gamelog,
):
    
    try:
        boxscore_href = gamelog.find(
            attrs={'data-stat': side}
        ).find('a').attrs['href']
        alias = boxscore_href.split('/')[2]
    except:
        alias = 'UNKNOWN'
    
    try:
        boxscore_text = gamelog.find(
            attrs={'data-stat': side}
        ).find('a').text
        market = boxscore_text.replace('.', '').replace('&', '').replace('(', '')
        market = market.replace(')', '').replace(' ', '-').lower().replace('*', '')
    except:
        market = 'UNKNOWN'

    return {
        f'{tm_or_opp}_alt_market': market,
        f'{tm_or_opp}_alt_alias': alias,
    }


def _locations(
    gamelog,
):

    location_text = gamelog.find(
        attrs={'data-stat': 'game_location'}
    ).text
    
    if location_text == '@':
        winner_location = 'A'
        loser_location = 'H'    
    elif location_text == '':
        winner_location = 'H'
        loser_location = 'A'    
    elif location_text == 'N':
        winner_location = 'N'
        loser_location = 'N'
    else:
        winner_location = 'N'
        loser_location = 'N'

    return {
        'tm_location': winner_location,
        'opp_location': loser_location,
    }


def _scores(
    gamelog,
):

    tm_score_text = gamelog.find(
        attrs={'data-stat': 'pts_win'}
    ).text
    
    opp_score_text = gamelog.find(
        attrs={'data-stat': 'pts_lose'}
    ).text
    
    try:
        tm_score = int(
            tm_score_text
        )
        opp_score = int(
            opp_score_text
        )
        return {
            'tm_score': tm_score,
            'opp_score': opp_score,
        }
    except ValueError:
        return {
            'tm_score': 0,
            'opp_score': 0,
        }


def _boxscore_stats_link(
    gamelog
):
    boxscore_stats_link_href = gamelog.find(
        attrs={'data-stat': 'boxscore_word'}
    ).find('a').attrs['href']
    
    boxscore_stats_link = f'https://www.pro-football-reference.com{boxscore_stats_link_href}'
    
    return {
        'boxscore_stats_link': boxscore_stats_link,
    }


def _gamelogs(
    season
):

    print('~'*100)
    print(f'Processing Season Gamelogs For: https://www.pro-football-reference.com/years/{season}/games.htm')
    print('~'*100)

    try:
        if season < 1970:
            print('~'*50)
            print('Gamelogs From 1970 to Present Only')
            print('~'*50)
            return pandas.DataFrame()
    except TypeError:
        print('~'*50)
        print('Season Should Be an Integer from 1970 to Present')
        print('~'*50)
        return pandas.DataFrame()

    try:
        res = requests.get(
            f'https://www.pro-football-reference.com/years/{season}/games.htm'
        )
    except requests.exceptions.RequestException:
        print('~'*100)
        print('Request Exception - Check Season Formatting')
        print('~'*100)
        return pandas.DataFrame()    

    dlist = []

    if res.status_code == 200:

        sleeptime = random.uniform(
            3.5, 
            5.5,
        )
        time.sleep(
            sleeptime
        )

        soup = BeautifulSoup(
            res.content, 
            'html.parser'
        )
        table = soup.find(
            'table',
            id='games'
        )
        tbody = table.find(
            'tbody'
        )
        table_rows = tbody.find_all(
            'tr'
        )

        for gamelog in table_rows:
            
            if not gamelog.attrs:

                if _is_playoff_filler(
                    gamelog
                ):
                    
                    week = _week(
                        season,
                        gamelog, 
                    )
                    week_day = _week_day(
                        gamelog
                    )
                    event_date = _event_date(
                        gamelog
                    )
                    tm_alt_alias_and_market = _alt_alias_and_market(
                        'tm', 
                        'winner', 
                        gamelog
                    )
                    opp_alt_alias_and_market = _alt_alias_and_market(
                        'opp', 
                        'loser', 
                        gamelog
                    )
                    tm_standardized = _standardized_with_side(
                        'tm',
                        tm_alt_alias_and_market.get('tm_alt_market'),
                    )
                    opp_standardized = _standardized_with_side(
                        'opp',
                        opp_alt_alias_and_market.get('opp_alt_market'),
                    )                    
                    locations = _locations(
                        gamelog
                    )
                    scores = _scores(
                        gamelog,
                    )
                    boxscore_stats_link = _boxscore_stats_link(
                        gamelog
                    )                 

                    if scores.get('tm_score') or scores.get('opp_score'):
                        status = 'closed'
                    else:
                        status = 'upcoming/postponed'

                    gamelog = {
                        'status': status,
                        'season': season,
                        **week,
                        **week_day,
                        **event_date,
                        **tm_standardized,
                        **tm_alt_alias_and_market,
                        **opp_standardized,
                        **opp_alt_alias_and_market,
                        **locations,
                        **scores,
                        **boxscore_stats_link,
                    }

                    dlist.append(
                        gamelog
                    )
        
    dset = pandas.DataFrame(
        dlist
    ).drop_duplicates()

    return dset