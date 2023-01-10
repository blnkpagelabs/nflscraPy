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


def _reference_teams(
    thead,
):

    home_tm = thead.find(
        attrs={'data-stat': 'home_team_score'}
    ).text

    vis_tm = thead.find(
        attrs={'data-stat': 'vis_team_score'}
    ).text

    return home_tm, vis_tm


def _trow_stat_info(
    trow,
):

    try:
        trow_stat_info = trow.find(
            attrs={"data-stat": "info"}
        ).text
    except:
        trow_stat_info = None
    
    return trow_stat_info


def _toss_data(
    trow,
):

    won_toss_text = trow.find(
        attrs={'data-stat': 'stat'}
    ).text
    won_toss_text = won_toss_text.replace(
        ' (deferred)'
        ,''
    ).lower()
    
    standardized = _standardized(
        won_toss_text
    )
    alias = standardized.get(
        'alias'
    )
    
    return alias


def _toss_decision(
    season,
    trow,
):

    decision = None

    won_toss_text = trow.find(
        attrs={'data-stat': 'stat'}
    ).text

    if won_toss_text:
        if season >= 2009:
            if 'deferred' in won_toss_text:
                decision = 'Deferred'
            else:
                decision = 'Accepted'
        else:
            decision = None
        
    return decision


def _roof_type(
    trow,
):

    roof_type = trow.find(
        attrs={'data-stat': 'stat'}
    ).text

    if roof_type:
        roof_type = roof_type.capitalize()

    return {
        'roof_type': roof_type
    }


def _surface_type(
    trow,
):

    surface_type = trow.find(
        attrs={'data-stat': 'stat'}
    ).text

    if surface_type:
        surface_type = surface_type.capitalize()

    return {
        'surface_type': surface_type
    }


def _duration(
    trow,
):

    duration_text = trow.find(
        attrs={'data-stat': 'stat'}
    ).text
    
    try:
        game_hours, game_minutes = duration_text.split(':')
        game_hours_in_minutes = int(game_hours) * 60
        duration = game_hours_in_minutes + int(game_minutes)
        return {
            'duration': duration
        }
    except ValueError:
        return {
            'duration': None
        }


def _attendance(
    trow,
):

    attendance = trow.find(
        attrs={'data-stat': 'stat'}
    ).text.replace(',', '')
    try:
        attendance = int(
            attendance
        )
        return {
            'attendance': attendance
        }        
    except ValueError:
        return {
            'attendance': None
        }


def _weather(
    trow,
):
    
    temperature, humidity_pct, wind_speed = None, None, None
    
    weather_text = trow.find(
        attrs={'data-stat': 'stat'}
    ).text
    
    weather_list = weather_text.split(',')

    for weather_text in weather_list:

        if 'degree' in weather_text:
            temperature = re.findall(
                r'\d+', 
                weather_text
            )
            temperature = float(temperature[0])

        if 'humidity' in weather_text:
            humidity_pct = re.findall(
                r'\d+', 
                weather_text
            )
            humidity_pct = float(humidity_pct[0])
 
        if 'mph' in weather_text:
            wind_speed = re.findall(
                r'\d+', 
                weather_text
            )
            wind_speed = float(wind_speed[0])

        if 'no wind' in weather_text:
            wind_speed = 0.0
    
    return {
        'temperature': temperature,
        'humidity_pct': humidity_pct,
        'wind_speed': wind_speed,
    }


def _vegas_spread_market(
    tm_text,
):
    vegas_spread_market = tm_text.replace('.', '').replace('&', '')
    vegas_spread_market = vegas_spread_market.replace('(', '').replace(')', '')
    vegas_spread_market = vegas_spread_market.replace(' ', '-').lower().replace('*', '')
    
    return vegas_spread_market


def _spreads(
    tm_standardized, 
    opp_standardized, 
    vegas_spread_and_total_text,
):

    vegas_spread_text = vegas_spread_and_total_text.get(
        'vegas_spread_text'
    )

    vegas_spread_text

    if vegas_spread_text == 'Pick' or vegas_spread_text == 'pick':
        tm_spread = 0.0
        opp_spread = 0.0
        return tm_spread, opp_spread

    tm_text = vegas_spread_text.split('-')
    tm_text = tm_text[0]
    tm_text = tm_text.strip()

    reference_team = _vegas_spread_market(
        tm_text
    )

    standardized = _standardized(
        reference_team
    )

    vegas_line_text = vegas_spread_text.split('-')
    vegas_line_text = vegas_line_text[-1]
    vegas_line = float(vegas_line_text) * -1

    if standardized.get('market') == tm_standardized.get('tm_market'):
        tm_spread = vegas_line
        opp_spread = vegas_line * -1

    if standardized.get('market') == opp_standardized.get('opp_market'):
        tm_spread = vegas_line * -1
        opp_spread = vegas_line

    return {
        'tm_spread': tm_spread,
        'opp_spread': opp_spread,
    }


def _total(
    vegas_spread_and_total_text,
):

    vegas_total_text = vegas_spread_and_total_text.get(
        'vegas_total_text'
    )

    try:
        total = re.findall(
            r"[-+]?(?:\d*\.\d+|\d+)", 
            vegas_total_text
        )
        total = float(total[0])
    except TypeError:
        total = None
        
    return {
        'total': total
    }


def _vegas_spread_and_total_text(
    comments,
):

    vegas_spread_text, vegas_total_text = None, None

    for comment in comments:

        if 'Vegas Line' in comment.extract():

            comment_soup = BeautifulSoup(
                comment.extract(), 
                'html.parser'
            )
            table_trs = comment_soup.find(
                'table', 
                id='game_info'
            ).find_all('tr')

            for tr in table_trs:
                try:
                    if tr.find('th').text == 'Vegas Line':
                        vegas_spread = tr.find('td')
                        vegas_spread_text = vegas_spread.text
                    if tr.find('th').text == 'Over/Under':
                        vegas_total = tr.find('td')
                        vegas_total_text = vegas_total.text
                except:
                    next

    return {
        'vegas_spread_text': vegas_spread_text,
        'vegas_total_text': vegas_total_text,
    }
    

def _gamelog_metadata(
    boxscore_stats_link, 
):
    
    try:
        season_and_event_date = _season_and_event_date(
            boxscore_stats_link,
        )
    except IndexError:
        print('~'*100)
        print('Unable to Process Gamelog Metadata - Check Boxscore Stats Link Formatting')
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

    print('~'*100)
    print(f'Processing Gamelog Metadata For: {boxscore_stats_link}')
    print('~'*100)

    meta = {
        'tm_spread': None,
        'opp_spread': None,
        'total': None,
        'attendance': None,
        'duration': None,
        'roof_type': None,
        'surface_type': None,
        'won_toss': None,
        'won_toss_decision': None,
        'won_toss_overtime': None,
        'won_toss_overtime_decision': None,
        'temperature': None,
        'humidity_pct': None,
        'wind_speed': None,
        'boxscore_stats_link': boxscore_stats_link,
    }

    res = requests.get(
        boxscore_stats_link
    )
    
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
        table = soup.find(
            'table',
            id='scoring'
        )
        thead = table.find(
            'thead'
        )
        reference_home_team, reference_vis_team = _reference_teams(
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
        vegas_spread_and_total_text = _vegas_spread_and_total_text(
            comments,
        )        
        spreads = _spreads(
            tm_standardized, 
            opp_standardized, 
            vegas_spread_and_total_text
        )
        total = _total(
            vegas_spread_and_total_text
        )
        meta = {
            **meta,
            **spreads,
            **total,
        }

        for comment in comments:

            if 'id="game_info"' in comment.extract():

                comment_soup = BeautifulSoup(
                    comment.extract(), 
                    'html.parser'
                )
                table = comment_soup.find(
                    'table'
                )
                trows = table.find_all(
                    'tr'
                )     

                for trow in trows:
                    
                    trow_stat_info = _trow_stat_info(
                        trow
                    )
                    
                    if trow_stat_info:
                        
                        if 'Won Toss' in trow_stat_info:
                            won_toss = _toss_data(
                                trow,
                            )
                            won_toss_decision = _toss_decision(
                                season_and_event_date.get(
                                    'season'
                                ),
                                trow,
                            )
                            meta['won_toss'] = won_toss
                            meta['won_toss_decision'] = won_toss_decision
                        if 'Won OT Toss' in trow_stat_info:
                            won_toss_overtime = _toss_data(
                                trow
                            )
                            won_toss_overtime_decision = _toss_decision(
                                season_and_event_date.get(
                                    'season'
                                ),
                                trow,
                            )
                            meta['won_toss_overtime'] = won_toss_overtime
                            meta['won_toss_overtime_decision'] = won_toss_overtime_decision
                        if 'Roof' in trow_stat_info:
                            roof_type = _roof_type(
                                trow
                            )
                            meta = {
                                **meta,
                                **roof_type,
                            }
                        if 'Surface' in trow_stat_info:
                            surface_type = _surface_type(
                                trow
                            )
                            meta = {
                                **meta,
                                **surface_type,
                            }
                        if 'Duration' in trow_stat_info:
                            duration = _duration(
                                trow
                            )
                            meta = {
                                **meta,
                                **duration,
                            }
                        if 'Attendance' in trow_stat_info:
                            attendance = _attendance(
                                trow
                            )
                            meta = {
                                **meta,
                                **attendance,
                            }
                        if 'Weather' in trow_stat_info:
                            weather = _weather(
                                trow
                            )
                            meta = {
                                **meta,
                                **weather,
                            }

        metadata = {
            **season_and_event_date,
            **tm_standardized,
            **opp_standardized,
            **meta,
        }

        dlist.append(
            metadata
        )

    dset = pandas.DataFrame(
        dlist
    )

    return dset