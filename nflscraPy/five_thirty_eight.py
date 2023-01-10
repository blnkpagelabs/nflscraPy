import pandas, numpy, requests, io, random, time
from .teams import _tms


def _standardized_by_tag(
    tag,
    reference_team,
):

    tms = _tms()

    by_tag = tms.get(
        reference_team.lower(), {}
    ).get(
        tag
    )

    return by_tag


def _five_thirty_eight():

    print('~'*100)
    print(f'Processing fiveThirtyEight Elo Dataset')
    print('~'*100)

    res = requests.get(
        'https://projects.fivethirtyeight.com/nfl-api/nfl_elo.csv', 
        stream=True
    )

    if res.status_code == 200:

        sleeptime = random.uniform(
            3.5, 
            5.5,
        )
        time.sleep(
            sleeptime
        )  

        dset = pandas.read_csv(
            io.BytesIO(res.content)
        )

        dset = dset[
            dset['season'] >= 1970
        ].reset_index(
            drop=True
        )

        dset = dset.replace({
            numpy.nan: None
        })

        for tag in (
            'nano',
            'market',
            'name',
            'alias',
        ):
            for side in (
                'team1',
                'team2',
            ):
                if side == 'team1':
                    tm_or_opp = 'tm'
                else:
                    tm_or_opp = 'opp'

                dset[f'{tm_or_opp}_{tag}'] = dset[side].apply(
                    lambda x: _standardized_by_tag(
                        tag,
                        x,
                    )
                )

        dset = dset[[
            'date',
            'season',
            'neutral',
            'playoff',
            'tm_nano',
            'tm_market',
            'tm_name',
            'tm_alias',
            'team1',
            'opp_nano',
            'opp_market',
            'opp_name',
            'opp_alias',
            'team2',
            'score1',
            'score2',
            'elo1_pre',
            'elo2_pre',
            'elo_prob1',
            'elo_prob2',
            'elo1_post',
            'elo2_post',
            'qbelo1_pre',
            'qbelo2_pre',
            'qb1',
            'qb2',
            'qb1_value_pre',
            'qb2_value_pre',
            'qb1_adj',
            'qb2_adj',
            'qbelo_prob1',
            'qbelo_prob2',
            'qb1_game_value',
            'qb2_game_value',
            'qb1_value_post',
            'qb2_value_post',
            'qbelo1_post',
            'qbelo2_post',
            'quality',
            'importance',
            'total_rating',
        ]]

        dset = dset.rename(
            columns={
                'date': 'event_date',
                'team1': 'tm_alt_alias',
                'team2': 'opp_alt_alias',
                'score1': 'tm_score',
                'score2': 'opp_score',
                'elo1_pre': 'tm_elo_pre',
                'elo2_pre': 'opp_elo_pre',
                'elo_prob1': 'tm_elo_win_prob',
                'elo_prob2': 'opp_elo_win_prob',
                'elo1_post': 'tm_elo_post',
                'elo2_post': 'opp_elo_post',
                'qbelo1_pre': 'tm_qb_elo_pre',
                'qbelo2_pre': 'opp_qb_elo_pre',
                'qb1': 'tm_qb',
                'qb2': 'opp_qb',
                'qb1_value_pre': 'tm_qb_elo_value_pre',
                'qb2_value_pre': 'opp_qb_elo_value_pre',
                'qb1_adj': 'tm_qb_elo_adj',
                'qb2_adj': 'opp_qb_elo_adj',
                'qbelo_prob1': 'tm_qb_elo_win_prob',
                'qbelo_prob2': 'opp_qb_elo_win_prob',
                'qb1_game_value': 'tm_qb_game_value',
                'qb2_game_value': 'opp_qb_game_value',
                'qb1_value_post': 'tm_qb_post_game_value',
                'qb2_value_post': 'opp_qb_post_game_value',
                'qbelo1_post': 'tm_qb_elo_post_game',
                'qbelo2_post': 'opp_qb_elo_post_game',
            }
        )

        return dset