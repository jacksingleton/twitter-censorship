import os.path
import util
import config

def _fetch_page(page):
    startat = page * 10
    response = requests.get(config.CHILLING_EFFECTS_URL + str(startat))
    source = response.text
    logger.debug('source=%s', source)
    return source

def _page_file_path(page):
    return os.path.join(config.STORE_DIR, 'table_pages', str(page))

def _load_page_from_file(page):
    with open(_page_file_path(page)) as fp:
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
            util.random_wait()
            yield _save_page(page, _fetch_page(page))
