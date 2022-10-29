#Improts 
import os
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from lib.download_data import download

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

path = "/workspaces/European-Soccer/Data/"  #Insert path here
database = path + "database.sqlite"

#if file does not exist, download it
if not os.path.exists(database):
    download()

