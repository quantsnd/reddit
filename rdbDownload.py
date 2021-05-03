from rdb import redditdb 
import datetime as dt
import os
from os import listdir
from os.path import isfile, join


r = redditdb(subreddit = "wallstreetbets", start = dt.datetime(2016,1,1), limit = None, path = '/Volumes/GoogleDrive/My Drive/QuantND reddit project/Data')

# updates to today's date at 0:00:00
now = dt.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
yesterday = now - dt.timedelta(days = 1)


r.updateAll(dt.datetime(2016,3,1))
