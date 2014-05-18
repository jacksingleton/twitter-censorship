import os.path
import logging

import requests

import util
import config

logger = logging.getLogger(__name__)

def _fetch_page(page):
    logger.info('page=%d from=http', page)
    util.random_wait()
    startat = page * 10
    response = requests.get(config.CHILLING_EFFECTS_URL + str(startat))
    logger.debug('source=%s', response.text)
    return response.text

def _page_file_path(page):
    return os.path.join(config.STORE_DIR, 'table_pages', str(page))

def _load_page_from_file(page):
    logger.info('page=%d from=file', page)
    with open(_page_file_path(page), encoding='utf-8') as fp:
        return fp.read()

def _already_downloaded_page(page):
    return os.path.isfile(_page_file_path(page))

def _save_page(page, source):
    with open(_page_file_path(page), 'w') as fp:
        fp.write(source)
    return source

LAST_PAGE = 1704

def fetch_table_pages():
    for page in range(0, LAST_PAGE + 1):
        if _already_downloaded_page(page):
            yield _load_page_from_file(page)
        else:
            yield _save_page(page, _fetch_page(page))
