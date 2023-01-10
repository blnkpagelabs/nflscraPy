import requests, pandas, time, random, re
from bs4 import BeautifulSoup, Comment
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

    reference_team = reference_team.lower()

    tm_tags = (
        'nano',
        'market',
        'name',
        'alias',
    )

    standardized = {
        tm_tag: tms.get(
            reference_team,
        ).get(
            tm_tag
        )
        for tm_tag in tm_tags
    }

    return standardized


def _reference_team(
    trow,
):

    reference_team = trow.find(
        attrs={'data-stat': 'team_name'}
    ).text
    
    return reference_team


def _expected_points_stat(
    tag,
    trow,
):

    expected_points_text = trow.find(
        attrs={'data-stat': tag}
    ).text

    try:
        expected_points_stat = float(expected_points_text)
    except ValueError:
        expected_points_stat = None

    return expected_points_stat


def _gamelog_expected_points(
    boxscore_stats_link,
):

    print('~'*100)
    print(f'Processing Expected Points For: {boxscore_stats_link}')
    print('~'*100)

    try:
        season_and_event_date = _season_and_event_date(
            boxscore_stats_link,
        )
    except IndexError:
        print('~'*100)
        print('Unable to Process Gamelog Statistics - Check Boxscore Stats Link Formatting')
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
        comments = soup.find_all(
            string = lambda text: isinstance(text, Comment)
        )
        
        for comment in comments:
            
            if 'id="expected_points"' in comment.extract():

                comment_soup = BeautifulSoup(
                    comment.extract(), 
                    'html.parser'
                )
                tbody = comment_soup.find(
                    'tbody'
                )
                trows = tbody.find_all(
                    'tr'
                )

                for trow in trows:

                    reference_team = _reference_team(
                        trow
                    )
                    standardized = _standardized(
                        reference_team,
                    )
                    metadata = {
                        **season_and_event_date,
                        **standardized,
                    }
                    stats = {
                        display: _expected_points_stat(
                            tag, 
                            trow
                        )
                        for display, tag in {
                            'exp_pts': 'pbp_exp_points_tot',
                            'exp_pts_off': 'pbp_exp_points_off_tot',
                            'exp_pts_off_pass': 'pbp_exp_points_off_pass',
                            'exp_pts_off_rush': 'pbp_exp_points_off_rush',
                            'exp_pts_off_turnover': 'pbp_exp_points_off_to',
                            'exp_pts_def': 'pbp_exp_points_def_tot',
                            'exp_pts_def_pass': 'pbp_exp_points_def_pass',
                            'exp_pts_def_rush': 'pbp_exp_points_def_rush',
                            'exp_pts_def_turnover': 'pbp_exp_points_def_to',
                            'exp_pts_st': 'pbp_exp_points_st',
                            'exp_pts_kickoff': 'pbp_exp_points_k',
                            'exp_pts_kick_return': 'pbp_exp_points_kr',
                            'exp_pts_punt': 'pbp_exp_points_p',
                            'exp_pts_punt_return': 'pbp_exp_points_pr',
                            'exp_pts_fg_xp': 'pbp_exp_points_fgxp',
                        }.items()
                    }
                    expected_points_stats = {
                        **metadata,
                        **stats,
                        'boxscore_stats_link': boxscore_stats_link,
                    }
                    dlist.append(
                        expected_points_stats
                    )

    dset = pandas.DataFrame(
        dlist
    )

    return dset