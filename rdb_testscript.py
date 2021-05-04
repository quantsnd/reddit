# short script explaining how to use the rdb library

from rdb import redditdb 
import datetime as dt
import os
from os import listdir
from os.path import isfile, join

# this creates a reddit data base object that contains the start date of when you want to start collecting information
# limit of comments per day is limit = 20 for the test script but can be set to None
test = redditdb(subreddit = "wallstreetbets", start = dt.datetime(2016,1,1), limit = None, path = '/Volumes/GoogleDrive/My Drive/QuantND reddit project/Data')

# saves all the comments and posts from the start date to the day previous to the current day 0:00:00

# loads a date range of dataframes as a dictionary { dt.datetime : pd.DataFrame }
dfComments, dfPosts = test.loadRangeAll(start = dt.datetime(2016,1,1), end = dt.datetime(2016,2,1))

print( dfComments, dfPosts )