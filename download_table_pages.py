#!/usr/bin/env python

import urllib2
import os.path
import util
import config

def _fetch_page(page):
    startat = page * 10
    return urllib2.urlopen(config.CHILLING_EFFECTS_URL + str(startat)).read()

def _page_file_path(page):
    return os.path.join(config.STORE_DIR, 'table_pages', str(page))

def _already_downloaded_page(page):
    return os.path.isfile(_page_file_path(page))

def _save_page(page, source):
    with open(_page_file_path(page), 'w') as fp:
        fp.write(source)

LAST_PAGE = 1704

for page in range(0, LAST_PAGE + 1):
    if _already_downloaded_page(page): continue

    print 'Downloading page starting at ' + str(page)
    _save_page(page, _fetch_page(page))

    util.random_wait()
