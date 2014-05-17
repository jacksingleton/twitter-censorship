#!/usr/bin/env python3

import os

import download_table_pages
import download_notices
import parse_notice_tweets
import find_censored_tweets

for path in ['store/table_pages', 'store/notices', 'store/tweets']:
    if not os.path.exists(path):
        os.mkdirs(path)

withheld_tweets = (tweet
    for table_page in download_table_pages.fetch_table_pages()
    for notice in download_notices.fetch_notices(table_page)
    for tweet in parse_notice_tweets.parse_tweets_from(notice)
    if find_censored_tweets.is_withheld(tweet))

for t in withheld_tweets: print(t)
