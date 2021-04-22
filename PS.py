import requests
import datetime as dt
from pmaw import PushshiftAPI
import pandas as pd

api = PushshiftAPI() 

# before = int(dt.datetime(2021,1,1).timestamp())
# after = int(dt.datetime(2020,12,1).timestamp())

before = int(dt.datetime(2021,2,1).timestamp())
after = int(dt.datetime(2021,1,1).timestamp())

subreddit="wallstreetbets"
limit=100

comments = api.search_comments(subreddit=subreddit, limit=limit, before=before, after=after)
print(f'Retrieved {len(comments)} comments from Pushshift')

comments_df = pd.DataFrame(comments)# preview the comments data
print(comments_df.index)
print(comments_df.head(10).loc[:,['created_utc', 'author', 'body']])

# comments_df.to_csv('./wsb_comments.csv', header=True, index=False, columns=list(comments_df.axes[1]))