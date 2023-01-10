import requests, pandas, time, random, numpy
from bs4 import BeautifulSoup, Comment
from .teams import _tms


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


def _split_definition_and_values(
    tag,
    trow,
):

    splits_by_definitions = {
        'game_location': 'Location',
        'qtr': 'Qtr',
        'down': 'Down',
        'yds_split': 'YdsToGo',
        'down_distance': 'DownsAndYdsToGo',
        'field_position': 'FieldPosition',
        'pt_diff': 'ScoreDifferential',
        'situation': 'GameSituation',
        'snap_type': 'SnapTypeAndHuddle',
        'blitz_type': 'PassRushType',
    }

    splits_definition = splits_by_definitions.get(
        tag,
        'Unknown',
    )

    splits_type = trow.find(
        attrs={'data-stat': tag}
    ).text

    if splits_type == '10+':
        splits_type = '>10'

    splits_type = splits_type.replace(
        ' ',
        ''
    )
    splits_type = splits_type.replace(
        ',',
        ''
    )

    return splits_definition, splits_type


def _splits_stat(
    tag,
    trow,
):

    splits_stat = None

    if tag in [
        'plays',
        'rush_att',
        'rush_yds',
        'rush_td',
        'rush_first_down',
        'pass_cmp',
        'pass_att',
        'pass_yds',
        'pass_td',
        'pass_int',
        'pass_sacked',
        'pass_first_down',
    ]:

        try:
            splits_stats_text = trow.find(
                attrs={'data-stat': tag}
            ).text
        except AttributeError:
            return None

        if splits_stats_text:
            try:
                splits_stat = int(
                    splits_stats_text
                )
            except ValueError:
                splits_stat = None
        else:
            splits_stat = None
    
    else:

        try:
            splits_stats_text = trow.find(
                attrs={'data-stat': tag}
            ).text
        except AttributeError:
            return None

        if splits_stats_text:
            try:
                splits_stat = float(
                    splits_stats_text
                )
            except ValueError:
                splits_stat = None

            if tag == 'pass_cmp_perc':
                try:
                    splits_stat = round((splits_stat / 100), 3)
                except ZeroDivisionError:
                    splits_stat = 0
        else:
            splits_stat = None

    return splits_stat


def _season_splits(
    season,
    reference_alias,
    for_or_against
):

    dlist = []

    if for_or_against == 'For' or for_or_against == 'for':
        for_or_against = 'For'
        splits_stats_link = f'https://www.pro-football-reference.com/teams/{reference_alias}/{season}_splits.htm'
    elif for_or_against == 'Against' or for_or_against == 'against':
        for_or_against = 'Against'
        splits_stats_link = f'https://www.pro-football-reference.com/teams/{reference_alias}/{season}_opp_splits.htm'
    else:
        print('~'*100)
        print('Unable to Process Season Splits - Check Parameters')
        print('~'*100)
        return pandas.DataFrame()

    print('~'*100)
    print(f'Processing Splits Stats For: {splits_stats_link}')
    print('~'*100)

    try:
        res = requests.get(
            splits_stats_link
        )
    except requests.exceptions.RequestException:
        print('~'*100)
        print('Request Exception - Check Splits Stats Link Formatting')
        print('~'*100)
        return pandas.DataFrame()

    standardized = _standardized(
        reference_alias
    )
    
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
            id='game_location_splits'
        )
        tbody = table.find(
            'tbody'
        )
        trows = tbody.find_all(
            'tr'
        )

        for trow in trows:

            split_statistics = {
                'season': season,
                **standardized,
            }
            
            splits_definition, splits_type = _split_definition_and_values(
                'game_location',
                trow,
            )

            split_statistics['splits_by'] = splits_definition
            split_statistics['splits_type'] = splits_type
            split_statistics['splits_side'] = for_or_against

            for display, tag in {
                'total_plays': 'plays',
                'yds_to_go': 'yds_to_go',
                'avg_yds_gained': 'yards',
                'rush_att': 'rush_att',
                'rush_yds': 'rush_yds',
                'rush_yds_per_att': 'rush_yds_per_att',
                'rush_tds': 'rush_td',
                'rush_first_downs': 'rush_first_down',
                'pass_cmp': 'pass_cmp',
                'pass_att': 'pass_att',
                'pass_cmp_pct': 'pass_cmp_perc',            
                'pass_yds': 'pass_yds',
                'pass_yds_per_att': 'pass_yds_per_att',
                'pass_adj_net_yds_per_att': 'pass_adj_net_yds_per_att',
                'pass_int': 'pass_int',
                'pass_tds': 'pass_td',
                'pass_first_downs': 'pass_first_down',
                'passer_rating': 'pass_rating',
                'times_sacked': 'pass_sacked',
            }.items():

                splits_stat = _splits_stat(
                    tag,
                    trow,
                )

                split_statistics[display] = splits_stat

            dlist.append(
                split_statistics
            )

        comments = soup.find_all(
            string = lambda text: isinstance(text, Comment)
        )
        
        for comment in comments:

            for split_type in [
                'id="qtr_splits"',
                'id="down_splits"',
                'id="yds_split_splits"',
                'id="down_distance_splits"',
                'id="field_position_splits"',
                'id="pt_diff_splits"',
                'id="situation_splits"',
                'id="snap_type_splits"',
                'id="blitz_type_splits"',
            ]:
            
                if split_type in comment.extract():

                    comment_soup = BeautifulSoup(
                        comment.extract(), 
                        'html.parser'
                    )
                    comment_table = comment_soup.find(
                        'table'
                    )
                    comment_tbody = comment_table.find(
                        'tbody'
                    )
                    comment_trows = comment_tbody.find_all(
                        'tr'
                    )

                    for comment_trow in comment_trows:    

                        split_statistics = {
                            'season': season,
                            **standardized,
                        }

                        splits_definitions_tags = {
                            'id="qtr_splits"' : 'qtr',
                            'id="down_splits"' : 'down',
                            'id="yds_split_splits"' : 'yds_split',
                            'id="down_distance_splits"' : 'down_distance',
                            'id="field_position_splits"' : 'field_position',
                            'id="pt_diff_splits"' : 'pt_diff',
                            'id="situation_splits"' : 'situation',
                            'id="snap_type_splits"' : 'snap_type',
                            'id="blitz_type_splits"' : 'blitz_type',
                        }

                        splits_definitions_tag = splits_definitions_tags.get(
                            split_type
                        )

                        splits_definition, splits_type = _split_definition_and_values(
                            splits_definitions_tag,
                            comment_trow,
                        )

                        split_statistics['splits_by'] = splits_definition
                        split_statistics['splits_type'] = splits_type
                        split_statistics['splits_side'] = for_or_against

                        for display, tag in {
                            'total_plays': 'plays',
                            'yds_to_go': 'yds_to_go',
                            'avg_yds_gained': 'yards',
                            'rush_att': 'rush_att',
                            'rush_yds': 'rush_yds',
                            'rush_yds_per_att': 'rush_yds_per_att',
                            'rush_tds': 'rush_td',
                            'rush_first_downs': 'rush_first_down',
                            'pass_cmp': 'pass_cmp',
                            'pass_att': 'pass_att',
                            'pass_cmp_pct': 'pass_cmp_perc',            
                            'pass_yds': 'pass_yds',
                            'pass_yds_per_att': 'pass_yds_per_att',
                            'pass_adj_net_yds_per_att': 'pass_adj_net_yds_per_att',
                            'pass_int': 'pass_int',
                            'pass_tds': 'pass_td',
                            'pass_first_downs': 'pass_first_down',
                            'passer_rating': 'pass_rating',
                            'times_sacked': 'pass_sacked',
                        }.items():

                            splits_stat = _splits_stat(
                                tag,
                                comment_trow,
                            )

                            split_statistics[display] = splits_stat

                        dlist.append(
                            split_statistics
                        )


    dset = pandas.DataFrame(
        dlist
    )

    dset = dset.replace({
        numpy.nan: None
    })

    dset['splits_stats_link'] = splits_stats_link

    return dset