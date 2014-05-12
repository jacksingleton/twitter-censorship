#!/usr/bin/env python

import os
import util
import urllib2
from bs4 import BeautifulSoup
import config

def notice_tweets_for(notice_id):
    notice_tweets_path = os.path.join(
        config.STORE_DIR, 'notice_tweets', notice_id)
    with open(notice_tweets_path) as fp:
        return [t for t in fp.read().split('\n') if len(t) > 0]

def check_withheld_on_twitter(tweet):
    try:
        tweet_response = urllib2.urlopen('http://' + tweet).read()
        util.random_wait()
        tweet_soup = BeautifulSoup(tweet_response)
        withheld_div = tweet_soup.find('div', class_='tweet-user-withheld')
        return bool(withheld_div)
    except urllib2.HTTPError:
        return False

def check_withheld_on_filesystem(tweet):
    def known_withheld_tweets():
        with open(os.path.join(config.STORE_DIR, 'tweets/withheld')) as fp:
            return fp.read().split('\n')
    def known_not_withheld_tweets():
        with open(os.path.join(config.STORE_DIR, 'tweets/not_withheld')) as fp:
            return fp.read().split('\n')

    if tweet in known_withheld_tweets():
        return True
    elif tweet in known_not_withheld_tweets():
        return False
    else:
        return None

def save_withheld_status(tweet, withheld):
    save_file = 'withheld' if withheld else 'not_withheld'
    with open(os.path.join(config.STORE_DIR, 'tweets', save_file), 'a') as fp:
        fp.write(tweet + '\n')

def is_withheld(tweet):
    withheld_from_filesystem = check_withheld_on_filesystem(tweet)
    if withheld_from_filesystem is None:
        withheld_from_twitter = check_withheld_on_twitter(tweet)
        save_withheld_status(tweet, withheld_from_twitter)
        return withheld_from_twitter
    else:
        return withheld_from_filesystem
