# reddit dataframe class
# wrapper for PMAW to store reddit data into daily dataframes

import os
from os import listdir
from os.path import isfile, join

from pmaw import PushshiftAPI
import pandas as pd
import datetime as dt
from datetime import timedelta 

class redditdb:
    def __init__(self, subreddit: str = None, start: dt.datetime = None, path: str = os.getcwd(), limit: int = None):
        self.api = PushshiftAPI() 
        self.subreddit = subreddit
        self.start = start
        self.path = path
        self.limit = limit
        self.fpath = os.path.join(self.path, self.subreddit)
        self.fpathComments = os.path.join(self.fpath, "comments")
        self.fpathPosts = os.path.join(self.fpath, "posts")

        self.dfComments_list = None
        self.dfPosts_list = None

    # get list of dataframes
    def updateListComments(self):
        self.dfComments_list = [f for f in listdir(self.fpathComments) if isfile(join(self.fpathComments, f))]

    def updateListPosts(self):
        self.dfPosts_list = [f for f in listdir(self.fpathPosts) if isfile(join(self.fpathPosts, f))]

    # updates comments and posts
    def updateAll(self, date: dt.datetime):
        if not os.path.isdir(self.fpath):
            os.makedirs(self.fpath)

        self.updateComments(date)
        self.updatePosts(date)

    # update set of comment dataframes to yesterday
    def updateComments(self, date: dt.datetime):
        # makes the directory if it doesn't already exist
        if not os.path.isdir(self.fpathComments):
            os.makedirs(self.fpathComments)
        # starts downloading
        self.getallComments(date)
    
    def updatePosts(self, date: dt.datetime):
        # makes the directory if it doesn't already exist
        if not os.path.isdir(self.fpathPosts):
            os.makedirs(self.fpathPosts)
        # starts downloading
        self.getallPosts(date)
        
    # save all data in a time range
    def getallComments(self, end: dt.datetime):
        self.updateListComments()
        print("Retrieving comment data from {}: {} to {}".format(self.subreddit, self.start, end))

        dset = set(self.dfComments_list)

        for i in range( int( (end-self.start).days ) + 1):
            day = self.start + dt.timedelta(days = i)

            # check if day is already accounted for, if not download the comment dataframe
            if not '{}.csv'.format(day.date()) in dset:
                print('\033[32m{}\033[37m comments has not been downloaded for {}/comments. Downloading...'. format(day.date(), self.subreddit))
                self.savedayComments(day = day)
            else:
                print('\033[31m{}\033[37m comments already exists in {}/comments'. format(day.date(), self.subreddit))

    def getallPosts(self, end: dt.datetime):
        self.updateListPosts()
        print("Retrieving post data from {}: {} to {}".format(self.subreddit, self.start, end))

        dset = set(self.dfPosts_list)

        for i in range( int( (end-self.start).days ) + 1):
            day = self.start + dt.timedelta(days = i)

            # check if day is already accounted for, if not download the post dataframe
            if not '{}.csv'.format(day.date()) in dset:
                print('\033[32m{}\033[37m posts has not been downloaded in {}/posts. Downloading...'. format(day.date(), self.subreddit))
                self.savedayPosts(day = day)
            else:
                print('\033[31m{}\033[37m posts already exists in {}/posts'. format(day.date(), self.subreddit))

    
    # helper function to save data by day
    def savedayComments(self, day: dt.datetime):
        # gets comments from PushShift using PMAW wrapper
        comments = self.api.search_comments(subreddit=self.subreddit, rate_limit = 20, limit=self.limit, before=int((day+dt.timedelta(days=1)).timestamp()), after=int(day.timestamp()))
        print(f'Retrieved {len(comments)} comments from Pushshift')

        # converts into a dataframe with utc as index
        comments_df = pd.DataFrame(comments)
        # extra check
        if not comments_df.empty:
            comments_df = comments_df.sort_values(by=['created_utc']).set_index(['created_utc'])
        
        # calls download function
        self.downloadComments(comments_df, day)
    
    # helper function to save data by day
    def savedayPosts(self, day: dt.datetime):
        # gets posts from PushShift using PMAW wrapper
        posts = self.api.search_submissions(subreddit=self.subreddit, rate_limit = 20, limit=self.limit, before=int((day+dt.timedelta(days=1)).timestamp()), after=int(day.timestamp()))
        print(f'Retrieved {len(posts)} posts from Pushshift')

        # converts into a dataframe with utc as index
        posts_df = pd.DataFrame(posts)
        # extra check
        if not posts_df.empty:
            posts_df = posts_df.sort_values(by=['created_utc']).set_index(['created_utc'])
        
        # calls download function
        self.downloadPosts(posts_df, day)


    # download the info into a dataframe
    # path/subreddit/date
    def downloadComments(self, df: pd.DataFrame, day: dt.datetime):
        # checks to see if a folder with the name of the subreddit already exists
        if not os.path.isdir(self.fpathComments):
            os.makedirs(self.fpathComments)
        
        # names the file the current day
        fname = '{}.csv'.format(day.date())

        #save the file
        df.to_csv(os.path.join(self.fpathComments, fname))
        
     # download the info into a dataframe
    # path/subreddit/date
    def downloadPosts(self, df: pd.DataFrame, day: dt.datetime):
        # checks to see if a folder with the name of the subreddit already exists
        if not os.path.isdir(self.fpathPosts):
            os.makedirs(self.fpathPosts)
        
        # names the file the current day
        fname = '{}.csv'.format(day.date())

        #save the file
        df.to_csv(os.path.join(self.fpathPosts, fname))

    # load dataframe into memory
    def loadDayComments(self, day: dt.datetime):
        # check if folder exists
 
        if not os.path.isdir(self.fpathComments):
            print('The folder for {}/comments does not exist'.format(self.subreddit))
            return pd.DataFrame()
        else:
            # get name of file for the date
            fname = '{}.csv'.format(day.date())
            loadpath = os.path.join(self.fpathComments, fname)
            # check for file
            if os.path.exists(loadpath):
                return pd.read_csv(loadpath) 
            else:
                print("\033[31m{}\033[37m does not exist in {}/posts".format(day.date(), self.subreddit))
                return pd.DataFrame()
    
    # load dataframe into memory
    def loadDayPosts(self, day: dt.datetime):
        # check if folder exists
 
        if not os.path.isdir(self.fpathPosts):
            print('The folder for {}/posts does not exist'.format(self.subreddit))
            return pd.DataFrame()
        else:
            # get name of file for the date
            fname = '{}.csv'.format(day.date())
            loadpath = os.path.join(self.fpathPosts, fname)
            # check for file
            if os.path.exists(loadpath):
                return pd.read_csv(loadpath) 
            else:
                print("\033[31m{}\033[37m does not exist in {}/posts".format(day.date(), self.subreddit))
                return pd.DataFrame()


    def loadRangeAll(self, start: dt.datetime, end: dt.datetime):
        return self.loadRangeComments(start, end), self.loadRangePosts(start, end)

    # return the combined dataframe
    def loadRangeComments(self, start: dt.datetime, end: dt.datetime):
        dfout = pd.DataFrame()
        for i in range( int( (end-start).days ) + 1):
            day = start + dt.timedelta(days = i)
            df = self.loadDayComments(day)
            
            if not df.empty:
                dfout = dfout.append(df)
        
        return dfout

    # return the combined dataframe
    def loadRangePosts(self, start: dt.datetime, end: dt.datetime):
        dfout = pd.DataFrame()
        for i in range( int( (end-start).days ) + 1):
            day = start + dt.timedelta(days = i)
            df = self.loadDayPosts(day)
            
            if not df.empty:
                dfout = dfout.append(df)
        
        return dfout
        



    