import praw
from datetime import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 7})

# initialization
# use your bot info
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     redirect_uri='')

sr = 'pennystocks'

# get reddit posts
subreddit = reddit.subreddit(sr)

print(subreddit.display_name)


# gets all comments
def get_comments(type, amount):
    all_comments = []
    if type == 'hot':
        for submission in subreddit.hot(limit=amount):
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                all_comments.append(comment)
    elif type == 'new':
        for submission in subreddit.new(limit=amount):
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                all_comments.append(comment)

    return all_comments


all_comments_hot = get_comments('hot', 20)
all_comments_new = get_comments('new', 100)

# counts ticker name
def count_ticker(ticker, all_comments):
    word_count = 0
    comment_words = {}
    for comment in all_comments:
        if comment.body.find(ticker) >= 0:
            word_count += 1
            if dt.fromtimestamp(comment.created_utc).strftime("%m/%d") not in comment_words:
                comment_words.update( { dt.fromtimestamp(comment.created_utc).strftime("%m/%d") : 1} )
            else:
                comment_words[dt.fromtimestamp(comment.created_utc).strftime("%m/%d")] += 1
    print(comment_words)
    print(word_count)
    lists = sorted(comment_words.items())
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.yticks(np.arange(min(y), max(y) + 1, 1.0))
    plt.show()


# popular words count
def word_count(all_comments):
    word_count = {}
    for comment in all_comments:
        words = comment.body.split()
        for word in words:
            wordi = ''.join(filter(str.isalpha, word))
            if wordi.isupper() and len(wordi) <= 4 and len(wordi) >= 2:
                if wordi in word_count.keys():
                    word_count[wordi] += 1
                else:
                    word_count.update( {wordi : 1} )
    return word_count


# print word_count
def print_word_count(word_count):
    sorted_dict = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    for item in sorted_dict:
        if item[1] >= 2:
            print('{} : {}'.format( item[0], item[1] ))

# count_ticker('SINT', all_comments)
whot = word_count(all_comments_hot)
wnew = word_count(all_comments_new)


# takout w2 from w1
def takeout(w1, w2):
    dict_out = {}
    for key in w1:
        if not(key in w2):
            dict_out.update( {key : w1[key]} )
    return dict_out

junk = { 'DD' : 1 , 'ER' : 1, 'FOMO' : 1, 'PM' : 1, 'AH' : 1,
         'RH' : 1, 'PR' : 1, 'PDT' : 1, 'OTC' : 1, 'TD' : 1,
         'US' : 1, 'OP' : 1, 'AM': 1, 'SELL' : 1, 'BUY' : 1,
         'THE' : 1, 'SARS' : 1, ' NY' : 1, ' YOLO' : 1, 'PT' : 1,
         'IMO' : 1, }

#print_word_count(whot)
print_word_count(takeout(wnew, junk) )


#print_word_count( takeout(whot, wnew) )
















