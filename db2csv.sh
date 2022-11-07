#!/bin/bash
# This script will convert the sqlite database to csv files
sqlite3 -header -csv /workspaces/European-Soccer/Data/database.sqlite "select * from League;" > League.csv
sqlite3 -header -csv /workspaces/European-Soccer/Data/database.sqlite "select * from Match;" > Match.csv