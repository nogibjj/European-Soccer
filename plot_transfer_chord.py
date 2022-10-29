# Improts
import os
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from libs.download_data import download
from libs.utils import transfer_matrix


def main():
    # if file does not exist, download it
    path = "/workspaces/European-Soccer/Data/"
    database = path + "database.sqlite"
    if not os.path.exists(database):
        download()

    # connect to database
    conn = sqlite3.connect(database)

    # read data from database
    Match = pd.read_sql(
        """SELECT 
                            league_id, season,
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
                            FROM Match;""",
        conn,
    ).dropna()

    League = pd.read_sql(
        """SELECT id, name
                            FROM League;""",
        conn,
    )
    conn.close()

    # get all the seasons in the dataset
    seasons = list(Match.season.unique().astype(str))

    for season in seasons[: len(seasons) - 1]:
        # new league is added in this season, thus can't plot
        if season == "2012/2013":
            continue
        matrix, names = transfer_matrix(season, seasons, Match, League)
        chord_diagram(
            matrix,
            names,
            gap=0.03,
            use_gradient=False,
            sort="size",
            directed=True,
            cmap=None,
            chord_colors=None,
            rotate_names=False,
            show=True,
            fontsize=6,
        )
        prefix = season.replace("/", "_")
        plt.savefig(f"chord_photo/{prefix}_chord_diagram.png")
        plt.close()


if __name__ == "__main__":
    main()
    print("Done")
