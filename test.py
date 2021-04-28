from rdb import rdb
import datetime as dt
import os
from os import listdir
from os.path import isfile, join

test = rdb(subreddit = "wallstreetbets", start = dt.datetime(2021,4,20), limit = 20)

# test.getday(dt.datetime(2021,4,1), limit = 100)
test.update()