# reddit dataframe class
# wrapper for PMAW to store reddit data into daily dataframes

import os
from os import listdir
from os.path import isfile, join

from pmaw import PushshiftAPI
import pandas as pd
import datetime as dt
from datetime import timedelta 

class rdb:
    def __init__(self, subreddit: str = None, start: dt.datetime = None, path: str = os.getcwd(), limit: int = None):
        self.api = PushshiftAPI() 
        self.subreddit = subreddit
        self.start = start
        self.path = path
        self.limit = limit
        self.fpath = os.path.join(self.path, self.subreddit)

        self.df_list = None

    # get list of dataframes
    def updateList(self):
        self.df_list = [f for f in listdir(self.fpath) if isfile(join(self.fpath, f))]

    # update set of dataframes to yesterday
    def update(self):
        # makes the directory if it doesn't already exist
        if not os.path.isdir(self.fpath):
            os.makedirs(self.fpath)

        # updates to today's date at 0:00:00
        now = dt.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        yesterday = now - dt.timedelta(days = 1)

        # starts downloading
        self.getall(yesterday)

        
    # save all data in a time range
    def getall(self, end: dt.datetime):
        self.updateList()
        print("Retrieving data from {}: {} to {}".format(self.subreddit, self.start, end))

        dset = set(self.df_list)

        for i in range( int( (end-self.start).days ) + 1):
            day = self.start + dt.timedelta(days = i)

            # check if day is already accounted for, if not download the dataframe
            if not '{}.csv'.format(day.date()) in dset:
                print('\033[32m{}\033[37m has not been downloaded for r/{}. Downloading...'. format(day.date(), self.subreddit))
                self.saveDay(day = day)
            else:
                print('\033[31m{}\033[37m already exists in r/{}'. format(day.date(), self.subreddit))
    
    # helper function to save data by day
    def saveDay(self, day: dt.datetime):
        # gets comments from PushShift using PMAW wrapper
        comments = self.api.search_comments(subreddit=self.subreddit, rate_limit = 20, limit=self.limit, before=int((day+dt.timedelta(days=1)).timestamp()), after=int(day.timestamp()))
        print(f'Retrieved {len(comments)} comments from Pushshift')

        # converts into a dataframe with utc as index
        comments_df = pd.DataFrame(comments)
        # extra check
        if not comments_df['created_utc'].empty:
            comments_df = comments_df.sort_values(by=['created_utc']).set_index(['created_utc'])
        
        # calls download function
        self.download(comments_df, day)


    # download the info into a dataframe
    # path/subreddit/date
    def download(self, df: pd.DataFrame, day: dt.datetime):
        # checks to see if a folder with the name of the subreddit already exists
        if not os.path.isdir(self.fpath):
            os.makedirs(self.fpath)
        
        # names the file the current day
        fname = '{}.csv'.format(day.date())

        #save the file
        df.to_csv(os.path.join(self.fpath, fname))
        

    # load dataframe into memory
    def loadDay(self, day: dt.datetime):
        # check if folder exists
        if not os.path.isdir(self.fpath):
            print('The folder for r/{} does not exist'.format(self.subreddit))
            return pd.DataFrame()
        else:
            # get name of file for the date
            fname = '{}.csv'.format(day.date())
            loadpath = os.path.join(self.fpath, fname)
            # check for file
            if os.path.exists(loadpath):
                return pd.read_csv(loadpath) 
            else:
                print("\033[31m{}\033[37m does not exist in {}".format(day.date(), self.subreddit))
                return pd.DataFrame()


    # return a dictionary { dt.datetime : df }
    def loadRange(self, start: dt.datetime, end: dt.datetime):
        dfdict = {}
        for i in range( int( (end-start).days ) + 1):
            day = start + dt.timedelta(days = i)
            df = self.loadDay(day)
            
            if not df.empty:
                dfdict[day] = df
        
        return dfdict


        



    