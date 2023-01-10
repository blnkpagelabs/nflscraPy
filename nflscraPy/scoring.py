import requests, pandas, time, random, re
from bs4 import BeautifulSoup
from .teams import _tms


def _season_and_event_date(
    boxscore_stats_link,
):

    date_regex =  re.findall(
        r'\d+',
        boxscore_stats_link
    )

    year = date_regex[0][0:4]
    month = date_regex[0][4:6]
    day = date_regex[0][6:8]

    if month == '01' or month == 1:
        season = int(year) - 1
        event_date = f'{year}-{month}-{day}'
    else:
        season = int(year)
        event_date = f'{year}-{month}-{day}'

    return {
        'season': season,
        'event_date': event_date,
    }


def _standardized(
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
        tm_tag: tms.get(
            reference_team.lower(),
        ).get(
            tm_tag
        )
        for tm_tag in tm_tags
    }

    return standardized


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
    

def _srf_home_vis_tms(
    thead,
):

    home_tm = thead.find(
        attrs={'data-stat': 'home_team_score'}
    ).text

    vis_tm = thead.find(
        attrs={'data-stat': 'vis_team_score'}
    ).text

    return home_tm, vis_tm


def _time(
    trow,
):

    trow_text = trow.find(
        attrs={'data-stat': 'time'}
    ).text
    
    try:
        game_minutes, game_seconds = trow_text.split(':')
        game_seconds_breakdown = int(game_minutes) * 60
        time = game_seconds_breakdown + int(game_seconds)
        
        return {
            'time': time
        }
    except ValueError:
        return {
            'time': None
        }


def _scoring_team(
    trow,
):

    scoring_team = trow.find(
        attrs={'data-stat': 'team'}
    ).text
    
    scoring_standardized = _standardized(
        scoring_team
    )

    scoring_team = scoring_standardized.get(
        'name'
    )

    return {
        'scoring_team': scoring_team,
    }


def _quarter(
    trow,
):

    quarter = trow.find(
        attrs={'data-stat': 'quarter'}
    ).text

    if quarter == 'OT' or quarter == 'ot':
        quarter = 5

    try:
        quarter = int(quarter)
        return {
            'quarter': quarter
        }
    except ValueError:
        return {
            'quarter': None
        }


def _description(
    trow,
):

    description = trow.find(
        attrs={'data-stat': 'description'}
    ).text
    
    return {
        'description': description
    }


def _scores(
    trow,
):

    tm_score = trow.find(
        attrs={'data-stat': 'home_team_score'}
    ).text

    opp_score = trow.find(
        attrs={'data-stat': 'vis_team_score'}
    ).text
    
    try:
        tm_score = int(
            tm_score
        )
        opp_score = int(
            opp_score
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


def _gamelog_scoring(
    boxscore_stats_link,
):

    print('~'*100)
    print(f'Processing Game Scoring For: {boxscore_stats_link}')
    print('~'*100)
    
    try:
        season_and_event_date = _season_and_event_date(
            boxscore_stats_link,
        )
    except IndexError:
        print('~'*100)
        print('Unable to Process Gamelog Snap Counts - Check Boxscore Stats Link Formatting')
        print('~'*100)
        return pandas.DataFrame()

    try:
        res = requests.get(
            boxscore_stats_link
        )
    except requests.exceptions.RequestException:
        print('~'*100)
        print('Request Exception - Check Boxscore Stats Link Formatting')
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
            id='scoring'
        )
        tbody = table.find(
            'tbody'
        )
        thead = table.find(
            'thead'
        )        
        trows = tbody.find_all(
            'tr'
        )
        reference_home_team, reference_vis_team = _srf_home_vis_tms(
            thead
        )
        tm_standardized = _standardized_with_side(
            'tm',
            reference_home_team,
        )
        opp_standardized = _standardized_with_side(
            'opp',
            reference_vis_team,
        )

        for trow in trows:

            quarter = _quarter(
                trow
            )
            time_of_score = _time(
                trow
            )
            scoring_team = _scoring_team(
                trow
            )
            description = _description(
                trow
            )

            scores = _scores(
                trow,
            )

            scoring_data = {
                **season_and_event_date,
                **tm_standardized,
                **opp_standardized,
                **quarter,
                **time_of_score,
                **scoring_team,
                **scores,
                **description,
                'boxscore_stats_link': boxscore_stats_link,
            }

            dlist.append(
                scoring_data
            )
                    
    dset = pandas.DataFrame(
        dlist
    )
    
    dset['quarter'].ffill(inplace=True)

    return dset