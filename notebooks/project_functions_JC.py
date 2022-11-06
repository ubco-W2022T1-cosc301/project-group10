import numpy as np
import pandas as pd

def load_and_process(path):

    # Load data, drop unused data
    df1 = pd.read_csv(path)
    df1.drop(df1[df1.playoff != 0].index)
    df1.drop(columns=["season","playoff"])
    df1.drop(columns=df1.columns[8:15])
    df1.drop(columns=["home_team_postgame_rating","away_team_postgame_rating","game_quality_rating", "game_importance_rating","game_overall_rating"])
    df1.drop(columns=["neutral","status"])
    
    # Load table for distance
    df_distances = pd.read_csv("../data/raw/nhl_distances.csv")
    
    # clean up distance table: shorten team names to abbreviations
    team_abbr = ["ANA", "ARI", "BOS", "BUF", "CGY", "CAR", "CHI", "COL",
                            "CBJ", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL",
                            "NSH", "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SJS",
                            "SEA", "STL", "TBL", "TOR", "VAN", "VEG", "WSH", "WPG"]
    df_distances.columns = ["Home"] + team_abbr
    df_distances['Home'] = team_abbr
    
    # get new column for distances
    home = list(df1['home_team_abbr'])
    away = list(df1['away_team_abbr'])
    dists = []
    for i in range(len(home)):
        # this is ugly.
        # basically, it's my terrible way of getting the distance between the two cities.
        # if this were in Excel, I'd use a VLOOKUP, but we don't have that here.
        # so this will have to do, unoptimized though it is.
        dist = list(df_distances.loc[df_distances["Home"]==home[i]][away[i]])[0]
        dists.append(dist)
    
    
    # add new columns
    df2 = (
        df1
        .assign(home_team_diff=df1["home_team_score"]-df1["away_team_score"])
        .assign(away_team_diff=df1["away_team_score"]-df1["home_team_score"])
    )
    df2.insert(len(df1.columns),"distance",tuple(dists),True)
    
    return df2