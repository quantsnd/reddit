# short script explaining how to use the rdb library

from rdb import redditdb 
import datetime as dt
import os
from os import listdir
from os.path import isfile, join

# this creates a reddit data base object that contains the start date of when you want to start collecting information
# limit of comments per day is limit = 20 for the test script but can be set to None
test = redditdb(subreddit = "wallstreetbets", start = dt.datetime(2021,5,1), limit = 20, path = '/Volumes/GoogleDrive/My Drive/QuantND reddit project/Data')

# saves all the comments and posts from the start date to the day previous to the current day 0:00:00
test.updateAll()

# loads a date range of dataframes as a dictionary { dt.datetime : pd.DataFrame }
dfdictComments, dfdictPosts = test.loadRangeAll(start = dt.datetime(2021,4,29), end = dt.datetime(2021,5,2))

print( dfdictComments.keys(), dfdictPosts.keys() )