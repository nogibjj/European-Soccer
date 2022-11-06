#!/usr/bin/env python3

# Improts
import os
import argparse
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from libs.download_data import download
from libs.utils import transfer_matrix, get_data, read_season


def main(parser):
    # if file does not exist, download it
    path = "/workspaces/European-Soccer/Data/"
    database = path + "database.sqlite"
    if not os.path.exists(database):
        download()

    #read in the season
    season = read_season(parser)

    #get data from database
    seasons, Match, League = get_data(database, season)

    #plot the chord diagram
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
    plt.show()
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", help="season to plot", type=str, default="2014/2015")
    main(parser)
    print("Done")
