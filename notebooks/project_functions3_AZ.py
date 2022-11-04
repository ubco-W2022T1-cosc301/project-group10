import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_process(path):
    
    # Load dataa
    df = pd.read_csv(path)
    
    df_winslosses = df.loc[df["date"].index.repeat(2),:].reset_index(drop=True)

    df_winslosses = (
                df_winslosses.drop(columns=["season", "neutral", "status"])
                .loc[df_winslosses["playoff"] == 0]
                .reset_index(drop=True)
    )


    df_winslosses["team"] = np.where(df_winslosses.index % 2, df_winslosses["away_team"], df_winslosses["home_team"] )
    df_winslosses["abbr"] = np.where(df_winslosses.index % 2, df_winslosses["away_team_abbr"], df_winslosses["home_team_abbr"] )

    df_winslosses["wins"] = 0
    df_winslosses["wins"] = np.where((df_winslosses["team"] == df_winslosses["home_team"]) & (df_winslosses["home_team_score"] > df_winslosses["away_team_score"]), df_winslosses["wins"]+1, df_winslosses["wins"])
    df_winslosses["wins"] = np.where((df_winslosses["team"] == df_winslosses["away_team"]) & (df_winslosses["away_team_score"] > df_winslosses["home_team_score"]), df_winslosses["wins"]+1, df_winslosses["wins"])

    df_winslosses["losses"] = 0
    df_winslosses["losses"] = np.where((df_winslosses["team"] == df_winslosses["home_team"]) & (df_winslosses["home_team_score"] < df_winslosses["away_team_score"]) & df_winslosses["ot"].isnull() , df_winslosses["losses"]+1, df_winslosses["losses"])
    df_winslosses["losses"] = np.where((df_winslosses["team"] == df_winslosses["away_team"]) & (df_winslosses["away_team_score"] < df_winslosses["home_team_score"]) & df_winslosses["ot"].isnull(), df_winslosses["losses"]+1 , df_winslosses["losses"])

    df_winslosses["otl"] = 0
    df_winslosses["otl"] = np.where((df_winslosses["team"] == df_winslosses["home_team"]) & (df_winslosses["home_team_score"] < df_winslosses["away_team_score"]) & df_winslosses["ot"].notnull() , df_winslosses["otl"]+1, df_winslosses["otl"])
    df_winslosses["otl"] = np.where((df_winslosses["team"] == df_winslosses["away_team"]) & (df_winslosses["away_team_score"] < df_winslosses["home_team_score"]) & df_winslosses["ot"].notnull() , df_winslosses["otl"]+1 , df_winslosses["otl"])


    df_winslosses = (
                df_winslosses.drop(columns=["home_team_abbr", "away_team_abbr", "playoff", "ot", "overtime_prob", "home_team_expected_points", "away_team_expected_points"])
                .sort_values(by=['team', 'date'], ascending=True)
                .reset_index(drop=True)
    )


    team_set = set(df_winslosses["team"])

    df_winslosses["game_num"] = 0

    df_winslosses["gf"] = 0
    df_winslosses["gf"] = np.where((df_winslosses["team"] == df_winslosses["home_team"]), df_winslosses["home_team_score"], df_winslosses["away_team_score"])
                               
    df_winslosses["ga"] = 0
    df_winslosses["ga"] = np.where((df_winslosses["team"] == df_winslosses["home_team"]), df_winslosses["away_team_score"], df_winslosses["home_team_score"])                                                           

    for team in team_set:
    
        count = 0
        wins = 0
        losses = 0
        otls = 0
        gf = 0
        ga = 0
    
        for index in df_winslosses.index:
            
            if (df_winslosses.loc[index, "team"] == team ):
            
                count += 1;
                wins += df_winslosses.loc[index, 'wins']
                losses += df_winslosses.loc[index, 'losses']
                otls += df_winslosses.loc[index, 'otl']
                gf += df_winslosses.loc[index, 'gf']
                ga += df_winslosses.loc[index, 'ga']
            
                df_winslosses.loc[index, 'game_num'] = count
                df_winslosses.loc[index, 'wins'] = wins
                df_winslosses.loc[index, 'losses'] = losses
                df_winslosses.loc[index, 'otl'] = otls
                df_winslosses.loc[index, 'gf'] = gf
                df_winslosses.loc[index, 'ga'] = ga
            
            
    df_winslosses['pts'] = (df_winslosses['wins'] * 2) + (df_winslosses['otl'])
    
    return df_winslosses
