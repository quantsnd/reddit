from rdb import redditdb 
import datetime as dt
import csv

# sample code of frequency analysis on a given month
test = redditdb(subreddit = "wallstreetbets", start = dt.datetime(2016,1,1), limit = None, path = '/Volumes/GoogleDrive/My Drive/QuantND reddit project/Data')
dfComments, dfPosts = test.loadRangeAll(start = dt.datetime(2016,1,1), end = dt.datetime(2016,2,1))

ticker_count = {}
# tally up the number of comments referencing a ticker per ticker
def tickerFrequency(tickers, body, ticker_count):
    words = str(body).split(' ')
    for word in words:
        if word in tickers:
            if word in ticker_count:
                ticker_count[word] += 1
            else:
                ticker_count[word] = 1
    return ticker_count

# create set of all tickers in tickers.txt
tickers = set()
with open('tickers.txt', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        tickers.add(row[0])

# applies tickerFrequency to all comments
dfComments.apply(lambda row: tickerFrequency(tickers, row['body'], ticker_count), axis=1)

# print count of all the tickers
print(ticker_count)

