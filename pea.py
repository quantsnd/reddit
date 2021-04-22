import requests
from pmaw import PushshiftAPI
import pandas as pd
import datetime as dt
from datetime import timedelta 

# creates set of tickers using tickers.txt
tickers = set(map(str.strip, open('tickers.txt')))

# creates set of tickers that is contained in the body of a comment
def wordList(wordlist):
    return list(set(wordlist.split()) & tickers)

# uses the wordList function, will be expanded on later/changed
def analyze( body: str ):
    return wordList(body)

class pea():
    def __init__(self, start: dt.datetime, end: dt.datetime, subreddit: str):
        self.start = start
        self.end = end
        self.subreddit = subreddit

        # initializing PMAW wrapper
        self.api = PushshiftAPI() 
        # slices the columns
        self.peadf = pd.DataFrame(columns = ['created_utc', 'author', 'body'])

    def __str__(self, limit = None):
        return "start: {}, end: {}, subreddit: {}".format(self.start, self.end, self.subreddit)
    
    # get dataframe with time in utc, author, and body of text
    def getdf(self, limit = None):
        # prints out basic info
        print(self)

        # uses PMAW to gather the info form PushShift
        comments = self.api.search_comments(subreddit=self.subreddit, rate_limit = 30, limit=limit, before=int(self.end.timestamp()), after=int(self.start.timestamp()))
        print(f'Retrieved {len(comments)} comments from Pushshift')
        comments_df = pd.DataFrame(comments)
        comments_df = comments_df.loc[:,['created_utc', 'author', 'body']]
        self.peadf = comments_df.sort_values(by=['created_utc']).set_index(['created_utc'])

        return self.peadf

    # adds another column with tickers that are present in the body
    def analyze_df(self):
        self.peadf['tickers'] = self.peadf.apply(lambda row : analyze(row['body']), axis = 1)
        return self.peadf

    
    
