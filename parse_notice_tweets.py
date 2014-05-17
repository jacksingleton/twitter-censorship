import os
from bs4 import BeautifulSoup
import re

def parse_tweets_from(notice_source):
    soup = BeautifulSoup(notice_source)
    notice = soup.find('table', border='1', width='100%', cellpadding='5')
    notice_text = str(notice).decode('utf-8')
    tweets = re.findall('twitter.com/[a-zA-Z0-9_]{1,15}/status/\d+', notice_text)
    tweet_pics = re.findall('pic.twitter.com/[a-zA-Z0-9]{10}', notice_text)
    return tweets + tweet_pics
