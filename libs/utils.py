import pandas as pd

#create a table with all the players and the leagues they played in the given season
def create_player_league_table(season, Match):
    #select the season
    matches = Match.loc[Match["season"] == season, :]
    #melt the dataframes to have the play-league pair
    league_player = matches.melt(id_vars = ["league_id", "season"], \
                    value_name="player_id", var_name="player").drop(['season', "player"], axis=1)
    #drop duplicated rows
    league_player = league_player.drop_duplicates('player_id').reset_index(drop=True)
    
    return league_player

# return the next season
def next_season(season, seasons):
    assert seasons.count(season) != 0, "Season not found"
    assert seasons.index(season) < len(seasons)-1, "Last season"
    return seasons[list(seasons).index(season) + 1]

#create a transfer table, the first column is the league from, the second is the league to
def compute_transfer(season, seasons, Match):
    #create the player-league table for two consecutive seasons
    player_league_table1 = create_player_league_table(season, Match)
    player_league_table2 = create_player_league_table(next_season(season, seasons), Match)

    #find the players that are in the two seasons
    players = pd.merge(player_league_table1, player_league_table2, on="player_id", how="inner", suffixes=("_1", "_2"))

    #find the players that are in the two seasons and in the different league
    transfer = players.loc[players["league_id_1"] != players["league_id_2"], :].drop(["player_id"], axis=1).reset_index(drop=True)
    return transfer

#compute the transfer matrix, and the name for each column
def transfer_matrix(season, seasons, Match, League):
    transfer = compute_transfer(season, seasons, Match)
    
    #create a transfer matrix
    matrix = pd.pivot_table(
        transfer, index=["league_id_1"], columns=["league_id_2"], aggfunc="size", fill_value=0
    )

    league_name = League.set_index("id")["name"].to_dict()
    names = [league_name[i] for i in matrix.columns]

    return matrix.values.tolist(), names

if __name__ == "__main__":
    print("This is a module, not a script")
    