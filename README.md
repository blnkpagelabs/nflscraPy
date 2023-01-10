# Welcome to `nflscraPy`

This package was inspired by the creators of `nflscrapR` and `nflfastR` and 
the tremendous influence they have had on the open-source NFL community

The functionality of `nflscraPy` was designed to allow Python users to easily ingest boxscore and 
seasonal data from publicly available resourses, in particular, Pro Football Reference

Hopefully this package builds upon the availabilty of open-source resources for the football and data analytics community

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Installation

`pip install nflscraPy`

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Request Limits

To Be Respectful of Pro Football Reference's Servers Each Function Incorporates Sleeps Between 3.5 to 5.5 Seconds After Every Request

Remove or Reduce these Intervals at Your Own Risk – Sports Reference & Cloudflare will Temporarily/Permanently Suspend Access if you Throttle Their Servers

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Table of Contents

- [Seasons](#seasons)
- [Metadata](#metadata)
- [Statistics](#statistics)
- [Expected Points](#expected-points)
- [Scoring](#scoring)
- [Roster](#roster)
- [Snap Counts](#snap-counts)
- [Season Splits](#season-splits)
- [FiveThirtyEight](#fivethirtyeight)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Seasons

```python
import nflscraPy

season_gamelogs = nflscraPy._gamelogs(
    2022
)
```

### Description:

Returns all Gamelogs & Boxscore Stats Links for every NFL Season

### History:

2000 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/Seasons)

**`status`**

The Status of the game: `upcoming/postponed` | `closed`

**`season`**

The Season's Year

**`week`**

The Week of the Game

**`week_day`**

Weekday of the Game

**`event_date`**

The Date of the Game

**`tm_nano`**

nflSlowPy Nano ID

**`tm_market`**

nflSlowPy Market

**`tm_name`**

nflSlowPy Name 

**`tm_alias`**

nflSlowPy Alias

**`tm_alt_market`**

Pro Football Reference Market 

**`tm_alt_alias`**

Pro Football Reference Alias

**`opp_nano`**

nflSlowPy Nano ID

**`opp_market`**

nflSlowPy Market

**`opp_name`**

nflSlowPy Name 

**`opp_alias`**

nflSlowPy Alias

**`opp_alt_market`**

Pro Football Reference Market

**`opp_alt_alias`**

Pro Football Reference Alias

**`tm_location`**

Tm's Location: `H` | `A` | `N`

**`opp_location`**

Opp's Location: `H` | `A` | `N`

**`tm_score`**

Tm's Full Game Score

**`opp_score`**

Opp's Full Game Score

**`boxscore_stats_link`**

The Gamelog's Primary Key

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Metadata

```python
import nflscraPy

gamelog_metadata = nflscraPy._gamelog_metadata(
    'https://www.pro-football-reference.com/boxscores/202212180jax.htm'
)
```

### Description:

Returns Stadium Information | Game Weather Conditions | Vegas Spreads & Totals | Coin Toss Outcomes

### History:

2000 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/Metadata)

**`season`**

The Season's Year

**`event_date`**

The Date of the Game

**`tm_nano`**

nflSlowPy Nano ID

**`tm_market`**

nflSlowPy Market

**`tm_name`**

nflSlowPy Name 

**`tm_alias`**

nflSlowPy Alias

**`opp_nano`**

nflSlowPy Nano ID

**`opp_market`**

nflSlowPy Market

**`opp_name`**

nflSlowPy Name 

**`opp_alias`**

nflSlowPy Alias

**`tm_spread`**

Consensus Closing Spread Per Pro Football Reference – a spread of `0` indicates the Game Was a Pk'em

**`opp_spread`**

Consensus Closing Spread Per Pro Football Reference – a spread of `0` indicates the Game Was a Pk'em

**`total`**

Consensus Closing Total Per Pro Football Reference

**`attendance`**

The Total Recorded Attendance For The Event

**`duration`**

The Duration of the Event in Minutes – a duration of 210 indicates the game lasted for 3:30 Hrs

**`roof_type`**

The Type of the Stadiums Roof (Where Applicable)

**`surface_type`**

The Type of the Stadiums Field Surface Type

**`won_toss`**

The Alias of the Team That Won the Opening Coin Toss

**`won_toss_decision`**

Whether the team that Won the Opening Coin Toss Deferred or Accepted the Opening Kickoff

History on Coin Toss Decisions From 2009 to Present

**`won_toss_overtime`**

The Alias of the Team That Won the Overtime Coin Toss

**`won_toss_overtime_decision`**

Whether the team that Won the Overtime Coin Toss Deferred or Accepted the Overtime Kickoff

History on Coin Toss Decisions From 2009 to Present. (Let's Be Honest, Every Team is Accepting This)

**`temperature`**

The Recorded Temperature of the Game in Fahrenheit

**`humidity_pct`**

The Recorded Humidity of the Game

**`wind_speed`**

The Recorded Wind Speed of the Game (Where Applicable - i.e., Indoor Fields Will Not Have Wind Speed)

**`boxscore_stats_link`**

The Gamelog's Primary Key

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Statistics

```python
import nflscraPy

gamelog_statistics = nflscraPy._gamelog_statistics(
    'https://www.pro-football-reference.com/boxscores/202212180jax.htm'
)
```

### Description:

Returns a Game's Basic Boxscore Statistics

### History:

2000 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/Stats)

### Attributes:

**`season`**

The Season's Year

**`event_date`**

The Date of the Game

**`nano`**

nflSlowPy Nano ID

**`market`**

nflSlowPy Market

**`name`**

nflSlowPy Name 

**`alias`**

nflSlowPy Alias

**`rush_att`**

Total Offensive Rushing Attempts

**`rush_yds`**

Total Offensive Rushing Yards

**`rush_tds`**

Total Offensive Rushing Touchdowns

**`pass_cmp`**

Total Offensive Passes Completed

**`pass_att`**

Total Offensive Passes Attempted

**`pass_cmp_pct`**

Ratio of Passes Completed to Attempts

**`pass_yds`**

Total Offensive Passing Yards

**`pass_tds`**

Total Offensive Passing Touchdowns

**`pass_int`**

Total Offensive Passing Interceptions

**`passer_rating`**

Team's Total Passer Rating

**`net_pass_yds`**

Total Offensive Passing Net Yards

**`total_yds`**

Overall Offensive Yards

**`times_sacked`**

Total Times That a Quarterback(s) Was Sacked For

**`yds_sacked_for`**

Total Yards That a Quarterback(s) Was Sacked For

**`fumbles`**

Total Fumbles – Includes Those That Were Recovered and Lost

**`fumbles_lost`**

Fumbles Lost and Recovered by Opponent's Defense

**`turnovers`**

Total Turnovers, Including Fumbles Lost and Interceptions

**`penalties`**

Total Number of Offensive and Defensive Penalties

**`penalty_yds`**

Total Number of Offensive and Defensive Penalty Yards

**`first_downs`**

Total Offensive First Downs

**`third_down_conv`**

Offensive Third Down Conversions

**`third_down_att`**

Offensive Third Down Attempts

**`third_down_conv_pct`**

Ratio of Third Down Conversions to Attempts

**`fourth_down_conv`**

Offensive Fourth Down Conversions

**`fourth_down_att`**

Offensive Fourth Down Attempts

**`fourth_down_conv_pct`**

Ratio of Fourth Down Conversions to Attempts

**`possesion_time`**

Total Offensive Possession Time in Seconds 

**`boxscore_stats_link`**

The Gamelog's Primary Key

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Expected Points

```python
import nflscraPy

gamelog_expected_points = nflscraPy._gamelog_expected_points(
    'https://www.pro-football-reference.com/boxscores/202212180jax.htm'
)
```

### Description:

Expected Points utilizes historic play-by-play data to estimate the 'point value' associated with the start of each play, based on down, distance to go, and field position

For further information on this please see Pro Football Reference's [Blog Post](https://www.sports-reference.com/blog/2012/03/features-expected-points/) on the topic

### History:

2000 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/ExpectedPoints)

### Attributes

**`season`**

The Season's Year

**`event_date`**

The Date of the Game

**`nano`**

nflSlowPy Nano ID

**`market`**

nflSlowPy Market

**`name`**

nflSlowPy Name 

**`alias`**

nflSlowPy Alias

**`exp_pts`**

Total Expected Points For the Game (Negative For Losing Team and Positive For Winning Team)

**`exp_pts_off`**

Total Offensive Expected Points

Formula = Rusing Offense + Passing Offense + Offensive Penalties

**`exp_pts_off_pass`**

Expected Points From Passing Offense Plays

**`exp_pts_off_rush`**

Expected Points From Rushing Offense Plays

**`exp_pts_off_turnover`**

Expected Points From Offense Turnovers

**`exp_pts_def`**

Total Defensive Expected Points

Formula = Rusing Defense + Passing Defense + Defensive Penalties

**`exp_pts_def_pass`**

Expected Points From Passing Defense Plays

**`exp_pts_def_rush`**

Expected Points From Rushing Defense Plays

**`exp_pts_def_turnover`**

Expected Points From Defense Turnovers

**`exp_pts_st`**

Total Sepecial Teams Expected Points

Formula = Kickoff + Kick Return + Punt + Punt Return + FGs + XPs

**`exp_pts_kickoff`**

Expected Points From Kickoffs

**`exp_pts_kick_return`**

Expected Points From Kick Returns

**`exp_pts_punt`**

Expected Points From Punt Plays

**`exp_pts_punt_return`**

Expected Points From Punt Return Plays

**`exp_pts_fg_xp`**

Expected Points From FGs and XPs

**`boxscore_stats_link`**

The Gamelog's Primary Key

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Scoring

```python
import nflscraPy

gamelog_roster = nflscraPy._gamelog_roster(
    'https://www.pro-football-reference.com/boxscores/202212180jax.htm'
)
```

### Description:

Returns the Quarter, Time, Description, of every Scoring Event During a Game

### History:

2000 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/Scoring)

**`season`**

The Season's Year

**`event_date`**

The Date of the Game

**`tm_nano`**

nflSlowPy Nano ID

**`tm_market`**

nflSlowPy Market

**`tm_name`**

nflSlowPy Name 

**`tm_alias`**

nflSlowPy Alias

**`opp_nano`**

nflSlowPy Nano ID

**`opp_market`**

nflSlowPy Market

**`opp_name`**

nflSlowPy Name 

**`opp_alias`**

nflSlowPy Alias

**`quarter`**

The Quarter In Which the Scored Occured

**`time`**

The Time on the Clock in Seconds When the Score Occured – a clock of 120 indicates there was 2 minutes remaining in the quarter when the score occurred. 

**`scoring_team`**

The nflSlowPy Alias Corresponding to the Scoring Team

**`tm_score`**

The Score of the Game's `tm` After the Scoring Event Occured

**`opp_score`**

The Score of the Game's `opp` After the Scoring Event Occured

**`description`**

The Description of the Scoring Event – Including the Player's invovled, the play type, and associated yardage of the scoring event.

**`boxscore_stats_link`**

The Gamelog's Primary Key

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Roster

```python
import nflscraPy

gamelog_roster = nflscraPy._gamelog_roster(
    'https://www.pro-football-reference.com/boxscores/202212180jax.htm'
)
```

### Description:

Returns the Roster of Active Players Across Both Teams For a Game

### History:

2000 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/Roster)

**`season`**

The Season's Year

**`event_date`**

The Date of the Game

**`nano`**

nflSlowPy Nano ID

**`market`**

nflSlowPy Market

**`name`**

nflSlowPy Name 

**`alias`**

nflSlowPy Alias

**`player_href`**

The Player's Pro Football Reference HREF – Useful as a Unique Player ID and to Scrape Additional Player Statistics Not Yet Covered by nflSlowPy

**`player`**

Player's First and Last Name Per Pro Football Reference

**`position`**

A Player's Primary Position Per Pro Football Reference

**`boxscore_stats_link`**

The Gamelog's Primary Key

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Snap Counts

```python
import nflscraPy

gamelog_snap_counts = nflscraPy._gamelog_snap_counts(
    'https://www.pro-football-reference.com/boxscores/202212180jax.htm'
)
```

### Description:

Returns the Offensive | Defensive | Special Teams Snap Counts and Percentages For a Game

### History:

2012 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/SnapCounts)

**`season`**

The Season's Year

**`event_date`**

The Date of the Game

**`nano`**

nflSlowPy Nano ID

**`market`**

nflSlowPy Market

**`name`**

nflSlowPy Name 

**`alias`**

nflSlowPy Alias

**`player_href`**

The Player's Pro Football Reference HREF – Useful as a Unique Player ID and to Scrape Additional Player Statistics Not Yet Covered by nflSlowPy

**`player`**

Player's First and Last Name Per Pro Football Reference

**`position`**

A Player's Primary Position Per Pro Football Reference

**`snap_count_offense`**

The Total Offensive Number of Snap Counts Taken by a Player

**`snap_count_offense_pct`**

The Percentage of Offensive Snap Counts Taken by a Player

Formula = Player Snap Counts / Total Offensive Plays

**`snap_count_defense`**

The Total Defensive Number of Snap Counts Taken by a Player

**`snap_count_defense_pct`**

The Percentage of Defensive Snap Counts Taken by a Player.

Formula = Player Snap Counts / Total Defensive Plays

**`snap_count_special_teams`**

The Total Special Teams Number of Snap Counts Taken by a Player

**`snap_count_special_teams_pct`**

The Percentage of Special Teams Snap Counts Taken by a Player.

Formula = Player Snap Counts / Total Special Teams Plays

**`boxscore_stats_link`**

The Gamelog's Primary Key

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)

## Season Splits

```python
import nflscraPy

szn_splits_for_tm = nflscraPy._season_splits(
    2022,
    'jax',
    'For',
)

szn_splits_against_tm = nflscraPy._season_splits(
    2022,
    'jax',
    'Against',
)
```

### Description:

Returns either the Offensive or Defensive Season Split Stats.

Splits are broken down by Game Location, Quarter, Yards To Go, Game Siutuation, and More

### History:

2000 to Present

### Downloads:

To Be Respectful of Pro Football Reference's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/Splits)

### Attributes:

**`season`**

The Season's Year

**`nano`**

nflSlowPy Nano ID

**`market`**

nflSlowPy Market

**`name`**

nflSlowPy Name 

**`alias`**

nflSlowPy Alias

**`splits_by`**

Scenario of the Split By: Location, Quarter, Down, Distance, Score Differential, Game Situation, and Play Type

**`splits_type`**

Individual Scenario of the Split

**`splits_side`**

Whether the Split Stats Reflect the Teams's Performance or Opponent's in any Given Scenario – `For` | `Against`

**`total_plays`**

Number of Plays For The Split

**`yds_to_go`**

Avg. Yards to Go

**`avg_yds_gained`**

Avg. Yards Gained

**`rush_att`**

Number of Rush Attempts

**`rush_yds`**

Number of Rush Yards

**`rush_yds_per_att`**

Number of Rush Yards Per Attempt

**`rush_tds`**

Number of Rushing Touchdowns

**`rush_first_downs`**

Number of Rushing First Downs

**`pass_cmp`**

Number of Passes Completed

**`pass_att`**

Number of Passes Attempts

**`pass_cmp_pct`**

Passing Completion Percentage

**`pass_yds`**

Number of Passing Yards

**`pass_yds_per_att`**

Number of Passing Yards Per Attempt

**`pass_adj_net_yds_per_att`**

Number of Net Adjusted Passing Yards Per Attempt

**`pass_int`**

Number of Passing Interceptions

**`pass_tds`**

Number of Passing Touchdowns

**`pass_first_downs`**

Number of Passing First Downs

**`passer_rating`**

Team Passer Rating

**`times_sacked`**

Number of Times Sacked

**`splits_stats_link`**

The Season Split's HREF

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)


## FiveThirtyEight

```python
import nflscraPy

five_thirty_eight = nflscraPy._five_thirty_eight()
```

### Description:

FiveThirtyEight's traditional model uses Elo ratings (a measure of strength based on head-to-head results and quality of opponent) to calculate teams’ chances of winning their regular-season games and advancing to and through the playoffs. Our quarterback-adjusted Elo model incorporates news reports to project likely starters for every upcoming game and uses our quarterback Elo ratings to adjust win probabilities for those games. A team’s current quarterback adjustment is based on its likely starter in its next game and how much better or worse that QB is than the team’s top starter. Full methodology »

[Full Methodology](https://fivethirtyeight.com/methodology/how-our-nfl-predictions-work/)

### History:

1970 to Present

### Downloads:

To Be Respectful of fiveThirtyEight's Servers Please Backfill with Historic Data Available in the Releases

[Downloads](https://github.com/blnkpagelabs/nflscraPy/releases/tag/FiveThirtyEight)

### Attributes:

**`season`**

The Season's Year

**`event_date`**

The Date of the Game

**`neutral`**

**`playoff`**

**`tm_nano`**

nflSlowPy Nano ID

**`tm_market`**

nflSlowPy Market

**`tm_name`**

nflSlowPy Name 

**`tm_alias`**

nflSlowPy Alias

**`tm_alt_alias`**

FiveThirtyEight Alias

**`opp_nano`**

nflSlowPy Nano ID

**`opp_market`**

nflSlowPy Market

**`opp_name`**

nflSlowPy Name 

**`opp_alias`**

nflSlowPy Alias

**`opp_alt_alias`**

FiveThirtyEight Alias - **Preserved Historicall**

**`tm_score`**

Tm's Full Game Score

**`opp_score`**

Opp's Full Game Score

**`tm_elo_pre`**

Tm's Pregame Elo Rating

**`opp_elo_pre`**

Opp's Pregame Elo Rating

**`tm_elo_win_prob`**

Tm's Pregame Win Probability

**`opp_elo_win_prob`**

Opp's Pregame Win Probability

**`tm_elo_post`**

Tm's Updated Postgame Elo Rating

**`opp_elo_post`**

Opp's Updated Pregame Elo Rating

**`tm_qb_elo_pre_game`**

Tm's Pregame Elo Rating w/ Quarterback Adjustment Incl.

**`opp_qb_elo_pre_game`**

Opp's Pregame Elo Rating w/ Quarterback Adjustment Incl.

**`tm_qb`**

Tm's Starting Quarterback

**`opp_qb`**

Opp's Starting Quarterback

**`tm_qb_elo_value_pre`**

Tm's Starting Quarterback Elo Pregame

**`opp_qb_elo_value_pre`**

Opp's Starting Quarterback Elo Pregame

**`tm_qb_elo_adj`**

Tm's Starting Quarterback Elo Adjustment

**`opp_qb_elo_adj`**

Opp's Starting Quarterback Elo Adjustment

**`tm_qb_elo_win_prob`**

Tm's Pregame Win Probability w/ Quarterback Adjustment Incl.

**`opp_qb_elo_win_prob`**

Opp's Pregame Win Probability w/ Quarterback Adjustment Incl.

**`tm_qb_game_value`**

Tm's QB Game Elo Value – Performance Based

**`opp_qb_game_value`**

Opp's QB Game Elo Value – Performance Based

**`tm_qb_post_game_value`**

Tm's Starting Quarterback Elo Postgame - Adjusted for Game Elo Performance

**`opp_qb_post_game_value`**

Opp's Starting Quarterback Elo Postgame - Adjusted for Game Elo Performance

**`tm_qb_elo_post_game`**

Tm's Updated Postgame Elo Rating w/ Quarterback Adjustment Incl.

**`opp_qb_elo_post_game`**

Opp's Updated Postgame Elo Rating w/ Quarterback Adjustment Incl.

**`quality`**

Quality is determined by the harmonic mean of the teams’ Elo ratings – Based on a 0-100 Scale

**`importance`**

Importance measures how much the result will alter playoff projections – Based on a 0-100 Scale

**`total_rating`**

The overall number is the average of the quality and importance values.
