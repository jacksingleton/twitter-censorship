#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
import re

def notice_source(notice_id):
    with open('notices/' + notice_id) as fp:
        return fp.read()

def parse_tweets_from(notice_source):
    soup = BeautifulSoup(notice_source)
    notice = soup.find('table', border='1', width='100%', cellpadding='5')
    notice_text = str(notice).decode('utf-8')
    tweets = re.findall('twitter.com/[a-zA-Z0-9_]{1,15}/status/\d+', notice_text)
    tweet_pics = re.findall('pic.twitter.com/[a-zA-Z0-9]{10}', notice_text)
    return tweets + tweet_pics

def save_tweets(notice_id, notice_tweets):
    with open('notice_tweets/' + notice_id, 'w') as fp:
        fp.write('\n'.join(notice_tweets) + '\n')

notice_ids = os.listdir('notices')

for notice_id in notice_ids:
    notice_tweets = parse_tweets_from(notice_source(notice_id))
    if len(notice_tweets) == 0:
        print 'Notice with no tweets: ' + notice_id
    else:
        save_tweets(notice_id, notice_tweets)
