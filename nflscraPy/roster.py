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


def _reference_team(
    caption,
):

    caption_text = caption.text
    
    reference_team = caption_text.replace(
        ' Starters Table', ''
    ).lower()

    return reference_team


def _player(
    trow,
):

    player = trow.find(
        attrs={'data-stat': 'player'}
    ).text
    
    return {
        'player': player
    }


def _player_reference(
    trow,
):

    try:
        player_href = trow.find(
            attrs={'data-stat': 'player'}
        ).find('a').attrs['href']
        return {
            'player_href': player_href
        }
    except AttributeError:
        return {
            'player_href': None
        }


def _position(
    trow,
):

    position = trow.find(
        attrs={'data-stat': 'pos'}
    ).text
        
    return {
        'position': position
    }


def _gamelog_roster(
    boxscore_stats_link,
):

    print('~'*100)
    print(f'Processing Game Roster For: {boxscore_stats_link}')
    print('~'*100)
    
    try:
        season_and_event_date = _season_and_event_date(
            boxscore_stats_link,
        )
    except IndexError:
        print('~'*100)
        print('Unable to Process Gamelog Roster - Check Boxscore Stats Link Formatting')
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

            for stat_side in ['id="vis_starters"', 'id="home_starters"']:
            
                if stat_side in comment.extract():

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
                    caption = comment_soup.find(
                        'caption'
                    )
                    reference_team = _reference_team(
                        caption
                    )
                    standardized = _standardized(
                        reference_team
                    )

                    for trow in trows:

                        player = _player(
                            trow
                        )
                        player_reference = _player_reference(
                            trow
                        )
                        position = _position(
                            trow
                        )
                        starting_roster = {
                            **season_and_event_date,
                            **standardized,
                            **player_reference,
                            **player,
                            **position,
                            'boxscore_stats_link': boxscore_stats_link,
                        }
                        dlist.append(
                            starting_roster
                        )
                    
    dset = pandas.DataFrame(
        dlist
    )

    return dset