#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
import urllib2
import util
import config

def _page_source_for(page):
    page_path = os.path.join(config.STORE_DIR, 'table_pages', page)
    with open(page_path) as fp:
        return fp.read()

def _notice_paths_for(page_source):
    soup = BeautifulSoup(page_source)
    table = soup.find('table', border='1', cellpadding='5', width='100%')
    links = table.find_all('a')
    notice_links = [ link for link in links if 'notice.cgi' in str(link) ]
    return [ link['href'] for link in notice_links ]

def _notice_id_from_path(notice_path):
    return notice_path.split('=')[-1]

def _notice_path_for(notice_id):
    return os.path.join(config.STORE_DIR, 'notices', notice_id)

def _already_downloaded_notice(notice_id):
    return os.path.isfile(_notice_path_for(notice_id))

def _load_notice_from_file(notice_id):
    with open(_notice_path_for(notice_id)) as fp:
        return fp.read()

def _fetch_notice(notice_path):
    fp = urllib2.urlopen('https://www.chillingeffects.org' + notice_path)
    return fp.read()

def _save_notice(notice_id, notice_source):
    with open(_notice_path_for(notice_id), 'w') as fp:
        fp.write(notice_source)
        return notice_source

def fetch_notices(table_page):
    for notice_path in _notice_paths_for(table_page):
        notice_id = _notice_id_from_path(notice_path)
        if _already_downloaded_notice(notice_id):
            yield _load_notice_from_file(notice_id)
        else:
            yield _save_notice(notice_id, _fetch_notice(notice_path))
            util.random_wait()

