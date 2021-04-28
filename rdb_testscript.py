# short script explaining how to use the rdb library

from rdb import rdb
import datetime as dt
import os
from os import listdir
from os.path import isfile, join

# this creates a reddit data base object that contains the start date of when you want to start collecting information
# limit of comments per day is limit = 20 for the test script but can be set to None
test = rdb(subreddit = "wallstreetbets", start = dt.datetime(2021,4,25), limit = 20)

# saves a particular day's comments as a csv
test.saveDay(dt.datetime(2021,4,1), limit = 100)

# saves all the comments from the start date to the day previous to the current day 0:00:00
test.update()

# loads a date range of dataframes as a dictionary { dt.datetime : pd.DataFrame }
dfdict = test.loadRange(start = dt.datetime(2021,4,24), end = dt.datetime(2021,4,27))

