import requests, pandas, time, random, numpy, re
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
    stat_text,
    thead, 
):

    reference_team = thead.find(
        attrs={'data-stat': stat_text}
    ).text
    reference_team = reference_team.lower()
    
    return reference_team


def _rush_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[1]
        rush_stats_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        rush_stats_text_split = rush_stats_text.replace('--', '-')
        rush_stats_text_split = rush_stats_text_split.split('-')
        rush_att = rush_stats_text_split[0]
        rush_att = int(rush_att)
        rush_yds = rush_stats_text_split[1]
        rush_yds = int(rush_yds)
        rush_tds = rush_stats_text_split[2]
        rush_tds = int(rush_tds)
        return {
            'rush_att': rush_att,
            'rush_yds': rush_yds,
            'rush_tds': rush_tds,
        }
    except ValueError:
        return {
            'rush_att': None,
            'rush_yds': None,
            'rush_tds': None,
        }
    

def _pass_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[2]
        pass_stats_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        pass_stats_text_split = pass_stats_text.replace('--', '-')
        pass_stats_text_split = pass_stats_text_split.split('-')
        pass_cmp = pass_stats_text_split[0]
        pass_cmp = int(pass_cmp)
        pass_att = pass_stats_text_split[1]
        pass_att = int(pass_att)
        pass_yds = pass_stats_text_split[2]
        pass_yds = int(pass_yds)
        pass_tds = pass_stats_text_split[3]
        pass_tds = int(pass_tds)
        pass_int = pass_stats_text_split[4]
        pass_int = int(pass_int)

        try:
            pass_cmp_pct = round((pass_cmp / pass_att), 3)
        except ZeroDivisionError:
            pass_cmp_pct = 0

        return {
            'pass_cmp': pass_cmp,
            'pass_att': pass_att,
            'pass_cmp_pct': pass_cmp_pct,
            'pass_yds': pass_yds,
            'pass_tds': pass_tds,
            'pass_int': pass_int,
        }

    except ValueError:
        return {
            'pass_cmp': None,
            'pass_att': None,
            'pass_cmp_pct': None,
            'pass_yds': None,
            'pass_tds': None,
            'pass_int': None,
        }


def _passer_rating(
    pass_stats,
):

    pass_cmp = pass_stats.get(
        'pass_cmp'
    )
    pass_att = pass_stats.get(
        'pass_att'
    )
    pass_yds = pass_stats.get(
        'pass_yds'
    )
    pass_tds = pass_stats.get(
        'pass_tds'
    )
    pass_int = pass_stats.get(
        'pass_int'
    )

    blocks = {
        'a': (pass_cmp / pass_att - .3) * 5,
        'b': (pass_yds / pass_att - 3) * .25,
        'c': pass_tds / pass_att * 20,
        'd': 2.375 - pass_int / pass_att * 25,
    }
    blocks = {
        block: min((value, 2.375))
        for block, value in blocks.items()
    }
    blocks = {
        block: max((value, 0))
        for block, value in blocks.items()
    }
    passer_rating = sum(blocks.values()) / 6 * 100
    passer_rating = round(
        passer_rating,
        3,
    )

    return {
        'passer_rating': passer_rating
    }


def _sack_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[3]
        sack_stats_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        sack_stats_text_split = sack_stats_text.split('-')
        times_sacked = sack_stats_text_split[0]
        times_sacked = int(times_sacked)
        yds_sacked_for = sack_stats_text_split[1]
        yds_sacked_for = int(yds_sacked_for)
        return {
            'times_sacked': times_sacked,
            'yds_sacked_for': yds_sacked_for,
        }
    except ValueError:
        return {
            'times_sacked': None,
            'yds_sacked_for': None,
        }


def _net_pass_yds(
    stat_text,
    tbody, 
):
    
    try:
        table_body_row = tbody[4]
        net_pass_yds = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        net_pass_yds = int(net_pass_yds)
        return {
            'net_pass_yds': net_pass_yds,
        }        
    except ValueError:
        return {
            'net_pass_yds': None,
        }


def _total_yds(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[5]
        total_yds = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        total_yds = int(total_yds)
        return {
            'total_yds': total_yds,
        }          
    except ValueError:
        return {
            'total_yds': None,
        }   


def _fumbles_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[6]
        sack_stats_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        sack_stats_text_split = sack_stats_text.split('-')
        fumbles = sack_stats_text_split[0]
        fumbles = int(fumbles)
        fumbles_lost = sack_stats_text_split[1]
        fumbles_lost = int(fumbles_lost)
        return {
            'fumbles': fumbles,
            'fumbles_lost': fumbles_lost,
        }   
    except ValueError:
        return {
            'fumbles': None,
            'fumbles_lost': None,
        }   


def _turnover_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[7]
        turnovers = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        turnovers = int(turnovers)
        return {
            'turnovers': turnovers,
        }          
    except ValueError:
        return {
            'turnovers': None,
        }  


def _penalty_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[8]
        penalty_stats_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        penalty_stats_text_split = penalty_stats_text.split('-')
        penalties = penalty_stats_text_split[0]
        penalties = int(penalties)
        penalty_yds = penalty_stats_text_split[1]
        penalty_yds = int(penalty_yds)
        return {
            'penalties': penalties,
            'penalty_yds': penalty_yds,
        }  
    except ValueError:
        return {
            'penalties': None,
            'penalty_yds': None,
        }  


def _first_downs_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[0]
        first_downs = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        first_downs = int(first_downs)
        return {
            'first_downs': first_downs,
        }
    except ValueError:
        return {
            'first_downs': None,
        }


def _third_down_stats(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[9]
        third_down_stats_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        third_down_stats_text_split = third_down_stats_text.split('-')
        third_down_conv = third_down_stats_text_split[0]
        third_down_conv = int(third_down_conv)
        third_down_att = third_down_stats_text_split[1]
        third_down_att = int(third_down_att)
        
        try:
            third_down_conv_pct = round((third_down_conv / third_down_att), 3)
        except ZeroDivisionError:
            third_down_conv_pct = 0

        return {
            'third_down_conv': third_down_conv,
            'third_down_att': third_down_att,
            'third_down_conv_pct': third_down_conv_pct,
        }

    except ValueError:
        return {
            'third_down_conv': None,
            'third_down_att': None,
            'third_down_conv_pct': None,
        }


def _fourth_down_stats(
    stat_text,
    tbody, 
):
    
    try:
        table_body_row = tbody[10]
        fourth_down_stats_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        fourth_down_stats_text_split = fourth_down_stats_text.split('-')
        fourth_down_conv = fourth_down_stats_text_split[0]
        fourth_down_conv = int(fourth_down_conv)
        fourth_down_att = fourth_down_stats_text_split[1]
        fourth_down_att = int(fourth_down_att)
        
        try:
            fourth_down_conv_pct = round((fourth_down_conv / fourth_down_att), 3)
        except ZeroDivisionError:
            fourth_down_conv_pct = 0
        
        return {
            'fourth_down_conv': fourth_down_conv,
            'fourth_down_att': fourth_down_att,
            'fourth_down_conv_pct': fourth_down_conv_pct,
        }

    except ValueError:
        return {
            'fourth_down_conv': None,
            'fourth_down_att': None,
            'fourth_down_conv_pct': None,
        }


def _time_of_possession(
    stat_text,
    tbody, 
):

    try:
        table_body_row = tbody[11]
        time_of_possession_text = table_body_row.find(
            attrs={'data-stat': stat_text}
        ).text
        minutes, seconds = time_of_possession_text.split(':')
        minutes = int(minutes)
        seconds = int(seconds)
        time_of_possession = (minutes * 60) + seconds
        return {
            'time_of_possession': time_of_possession,
        }
    except ValueError:
        return {
            'time_of_possession': None,
        }


def _gamelog_statistics(
    boxscore_stats_link,
):

    print('~'*100)
    print(f'Processing Gamelog Statistics For: {boxscore_stats_link}')
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
            
            if 'id="team_stats"' in comment.extract():

                comment_soup = BeautifulSoup(
                    comment.extract(), 
                    'html.parser'
                )
                thead = comment_soup.find(
                    'thead'
                ).find(
                    'tr'
                )
                tbody = comment_soup.find(
                    'tbody'
                ).find_all(
                    'tr'
                )
                
                for stat_side in ['vis_stat', 'home_stat']:
                    
                    reference_team = _reference_team(
                        stat_side,
                        thead,
                    )
                    standardized = _standardized(
                        reference_team,
                    )
                    rush_stats = _rush_stats(
                        stat_side,
                        tbody,
                    )
                    pass_stats = _pass_stats(
                        stat_side,
                        tbody,
                    )
                    passer_rating = _passer_rating(
                        pass_stats,
                    )                    
                    net_pass_yds = _net_pass_yds(
                        stat_side,
                        tbody,
                    )
                    total_yds = _total_yds(
                        stat_side,
                        tbody,
                    )
                    sack_stats = _sack_stats(
                        stat_side,
                        tbody,
                    )
                    fumbles_stats = _fumbles_stats(
                        stat_side,
                        tbody,
                    )
                    turnover_stats = _turnover_stats(
                        stat_side,
                        tbody,
                    )
                    penalty_stats = _penalty_stats(
                        stat_side,
                        tbody,
                    )
                    first_downs_stats = _first_downs_stats(
                        stat_side,
                        tbody,
                    )                    
                    third_down_stats = _third_down_stats(
                        stat_side,
                        tbody,
                    )
                    fourth_down_stats = _fourth_down_stats(
                        stat_side,
                        tbody,
                    )
                    time_of_possession = _time_of_possession(
                        stat_side,
                        tbody,
                    )

                    statistics = {
                        **season_and_event_date,
                        **standardized,
                        **rush_stats,
                        **pass_stats,
                        **passer_rating,
                        **net_pass_yds,
                        **total_yds,
                        **sack_stats,
                        **fumbles_stats,
                        **turnover_stats,
                        **penalty_stats,
                        **first_downs_stats,
                        **third_down_stats,
                        **fourth_down_stats,
                        **time_of_possession,
                        'boxscore_stats_link': boxscore_stats_link,
                    }

                    dlist.append(
                        statistics
                    )

    dset = pandas.DataFrame(
        dlist
    )
    
    dset = dset.replace({
        numpy.nan: None
    })

    return dset