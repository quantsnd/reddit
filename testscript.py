# test file for the pea class
from collections import Counter
from pea import pea
import datetime as dt
import os

# initializing a pea object, start and end date to analyze and subreddit
test = pea(start = dt.datetime(2021,4,1), end = dt.datetime(2021,4,2), subreddit="wallstreetbets")

# creates initial dataframe with utc, author, and body of text from comment
# limit number of post, can be set to none
test.getdf( limit = 100 )
# adds a row the the df that contains the a set of ticker symbols the body of text contains
df = test.analyze_df()
print(df)

# dictionary of tickers and frequency
tickerslist = df['tickers'].tolist()
flat_list = [item for sublist in tickerslist for item in sublist]
print(Counter(flat_list))

path = 'wsb'
# saves the df as a csv
df.to_csv(os.path.join(path,'test.csv'))