#!/usr/bin/env python3

# Improts
import argparse
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from libs.utils import transfer_matrix, get_data, read_season


def main(par):
    # read in the season
    season = read_season(par)

    # get data from database
    database = "mids-367807.european_soccer"
    seasons, Match, League = get_data(database, season)

    # get the transfer matrix
    matrix, names = transfer_matrix(season, seasons, Match, League)

    # plot the chord diagram
    print("---------------Plotting chord diagram---------------")
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
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--season", help="season to plot", type=str, default="2014/2015"
    )
    main(parser)
    
