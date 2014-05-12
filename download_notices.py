#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
import urllib2
import util


def page_source_for(page):
    page_path = 'table_pages/' + page
    with open(page_path) as fp:
        return fp.read()

def notice_paths_for(page_source):
    soup = BeautifulSoup(page_source)
    table = soup.find('table', border='1', cellpadding='5', width='100%')
    links = table.find_all('a')
    notice_links = [ link for link in links if 'notice.cgi' in str(link) ]
    return [ link['href'] for link in notice_links ]

def notice_id(notice_path):
    return notice_path.split('=')[-1]

def already_downlaoded_notice(notice_id):
    return os.path.isfile('notices/' + notice_id)

def fetch_notice(notice_path):
    fp = urllib2.urlopen('https://www.chillingeffects.org' + notice_path)
    return fp.read()

def save_notice(notice_id, notice_source):
    with open('notices/' + notice_id, 'w') as fp:
        fp.write(notice_source)


downloaded_table_pages = os.listdir('table_pages')

page_sources = [ page_source_for(page) for page in downloaded_table_pages ]

notice_paths_per_page = [ notice_paths_for(page_source) for page_source in page_sources ]

notice_paths = util.flatten(notice_paths_per_page)

for notice_path in notice_paths:
    if already_downlaoded_notice(notice_id(notice_path)): continue

    print 'Downloading notice ' + notice_path
    save_notice(notice_id(notice_path), fetch_notice(notice_path))

    util.random_wait()
