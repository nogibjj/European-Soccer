import pandas as pd
import sqlite3

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

# get data from database
def get_data(database, season = "2011/2012"):
    # connect to database
    conn = sqlite3.connect(database)
    seasons = pd.read_sql("""   SELECT DISTINCT season
                                FROM Match;""", conn).values.flatten().tolist()

    # read data from database
    Match = pd.read_sql(
        f"""SELECT league_id, season,
                home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, 
                home_player_9, home_player_10, home_player_11, home_player_X1, home_player_X2, home_player_X3, 
                home_player_X4, home_player_X5, home_player_X6, home_player_X7, home_player_X8, home_player_X9, 
                home_player_X10, home_player_X11, home_player_Y1, home_player_Y2, home_player_Y3, home_player_Y4, 
                home_player_Y5, home_player_Y6, home_player_Y7, home_player_Y8, home_player_Y9, home_player_Y10, 
                home_player_Y11, 
                away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8,
                away_player_9, away_player_10, away_player_11, away_player_X1, away_player_X2, away_player_X3,
                away_player_X4, away_player_X5, away_player_X6, away_player_X7, away_player_X8, away_player_X9,
                away_player_X10, away_player_X11, away_player_Y1, away_player_Y2, away_player_Y3, away_player_Y4,
                away_player_Y5, away_player_Y6, away_player_Y7, away_player_Y8, away_player_Y9, away_player_Y10,
                away_player_Y11
            FROM Match
            WHERE season IN {season, next_season(season, seasons)};""",
        conn,
    ).dropna()

    League = pd.read_sql(
        """ SELECT id, name
            FROM League;""",
        conn,
    )
    conn.close()
    return seasons, Match, League

#read season from command line
def read_season(parser):
    args = parser.parse_args()
    season = args.season
    assert season!="2012/2013", "2012/2013 is not a valid season"
    return season

if __name__ == "__main__":
    print("This is a module, not a script")
    