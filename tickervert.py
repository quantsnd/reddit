# simple script to create textfile for the tickers
import pandas as pd
import csv

df1 = pd.read_csv ('./nasdaq_screener_1619017134186.csv')
df2 = pd.read_csv ('./nasdaq_screener_1619017163838.csv')
df3 = pd.read_csv ('./nasdaq_screener_1619017182789.csv')

tickers1 = set(df1['Symbol'])
tickers2 = set(df2['Symbol'])
tickers3 = set(df3['Symbol'])

tickerz = [tickers1, tickers2, tickers3]

all_tickers = set()

for item in tickerz:
    all_tickers.update(item)

def s(str):
    return str.strip()

all_tickers = set(map(s, all_tickers))
print(all_tickers)

with open("tickers.txt","w") as f:
    wr = csv.writer(f,delimiter="\n")
    wr.writerow(list(all_tickers))