import numpy as np
import pandas as pd
import seaborn as sns

def load_and_process(path):
    

    df = pd.read_csv(path)

    # Changed null values in ot column to 'reg' because null values break a lot of things
    df.loc[(df['ot'].isnull()), 'ot'] = 'reg'

    # Wanting to evaluate each game from both team's sides, so need to repeat each game so it can count
    # as a W for one team, and an L/OTL for the other team
    df = df.loc[df["date"].index.repeat(2),:].reset_index(drop=True)

    # Dropping season column because only analyzing 2021-2022 season
    # Dropping neutral column because no games were played at a neutral arena
    # Dropping status column because every game has been played already
    # Only including regular season games so every team can be equally evaluated
    df = (df.drop(columns=["season", "neutral", "status"])
            .loc[df["playoff"] == 0]
            .reset_index(drop=True)
    )

    # Adding team and abbreviation column because we are analyzing each team separately
    df["team"] = np.where(df.index % 2, df["away_team"], df["home_team"] )
    df["abbr"] = np.where(df.index % 2, df["away_team_abbr"], df["home_team_abbr"] )

    # Sort table to have blocks of each team's season ordered by the date
    df = (df.sort_values(by=['team', 'date'], ascending=True)
            .reset_index(drop=True)
    )

    # Drop playoff column since we are only looking at regular season games
    df = df.drop(columns=['playoff'])

    # Renaming some columns so they aren't so long
    df.rename(columns={"home_team_pregame_rating": "home_pre_rating",
                   "away_team_pregame_rating": "away_pre_rating",
                   "home_team_winprob": "home_winprob",
                   "away_team_winprob": "away_winprob",
                   "home_team_score": "home_score",
                   "away_team_score": "away_score",
                   "home_team_postgame_rating": "home_post_rating",
                   "away_team_postgame_rating": "away_post_rating"
                  })

    # Adding in a game number count by populating a list with 1-82 repeating for total table size
    # then adding it in as a column
    count = 1
    gameCount = []
    for i in range(1,2625):
        if count==83:
            count = 1
        gameCount.append(count)
        count += 1
    df['game_num'] = gameCount


    # add in days of rest between games for analysis!
    # Easiest way is to append date of last game onto row and subtract them from eachother, so append
    # previous game's date by using shift function

    # First, need to convert date from string to DateTime to allow for operations to be complete on dates
    df['date'] = pd.to_datetime(df['date'])
    df['last_game_date'] = df['date'].shift()

    # Based on how the spreadsheet is laid out, there is an issue where the first game of each team will
    # be taking the last game of the previous team. Fixed this by setting team's first game to NaN
    df.loc[df['game_num'] == 1, 'last_game_date'] = np.nan
    
    df['team_rating'] = np.where(df["abbr"]==df["home_team_abbr"], df['home_team_pregame_rating'], df['away_team_pregame_rating'])
    df['opposing_team_rating'] = np.where(df["abbr"]==df["home_team_abbr"], df['away_team_pregame_rating'], df['home_team_pregame_rating'])

    df['team_rating'] = df['team_rating'].astype('float64')
    df['opposing_team_rating'] = df['opposing_team_rating'].astype('float64')
    
    df['rating_diff'] = df['team_rating'] - df['opposing_team_rating']
    
    df['gf'] = np.where(df["abbr"]==df["home_team_abbr"], df['home_team_score'], df['away_team_score'])
    df['ga'] = np.where(df["abbr"]==df["home_team_abbr"], df['away_team_score'], df['home_team_score'])

    #Calculate rest days by subtracting game date by last game date
    df['rest_days'] = np.where(df['last_game_date']!= np.nan, ((df['last_game_date'] - df['date'])*-1).dt.days, "NA")
    df['rest_days'] = df['rest_days'].astype('string')

    #Need to add outcomes of Games with a couple where statements
    df['game_outcome'] = np.where((df["abbr"]==df["home_team_abbr"]) & (df["home_team_score"] > df["away_team_score"]) | (df["abbr"]==df["away_team_abbr"]) & (df["away_team_score"] > df["home_team_score"]), "W", "L")
    df['game_outcome'] = np.where((df['game_outcome']=="L") & (df['ot'] != 'reg'), 'OTL', df['game_outcome'])

    return df
    

    