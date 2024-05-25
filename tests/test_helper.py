import logging
import os

import httpretty


def setup_logger():
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logging.getLogger('pynamodb').setLevel(logging.CRITICAL)
    logging.getLogger('pynamodb.settings').setLevel(logging.CRITICAL)

    logging.basicConfig()
    logger = logging.getLogger(__name__)

    # Change logging level here.
    logger.setLevel(os.environ.get('LOG_LEVEL', logging.INFO))


def data_file_path(file_name):
    if os.path.isfile(f"tests/{file_name}"):
        return f"tests/{file_name}"
    return file_name


def register_url(content_file,
                 url,
                 match_querystring=True,
                 status=200,
                 headers=None,
                 method=httpretty.GET):
    if headers is None:
        headers = {}
    content_type = None
    if content_file.endswith(".htm") or content_file.endswith(".html"):
        content_type = 'text/html; charset=UTF-8'
    elif content_file.endswith(".json"):
        content_type = 'application/json; charset=UTF-8'
    elif content_file.endswith(".js"):
        content_type = 'text/javascript; charset=UTF-8'
    if content_type is not None:
        headers = {**headers,  # We need this so requests can know the proper file encoding
                   'Content-Type': content_type}
    with open(data_file_path(content_file), "r") as _file:
        content = _file.read()
    print("REGISTER " + url + " file: " + content_file)
    httpretty.register_uri(method,
                           url,
                           body=content,
                           match_querystring=match_querystring,
                           content_type=content_type,
                           status=status,
                           **headers)


def register_redirect(url, redirect_location):
    register_url("data/globe-tracker-redirect.html",
                 url,
                 status=301,
                 headers={"Location": redirect_location})
    register_url("data/globe-tracker-redirect.html", redirect_location)


def register_urls():
    print("Registering URLS")
    httpretty.HTTPretty.allow_net_connect = False
    httpretty.enable()
    register_url("data/businesswire.com_news_feed.html", "https://www.businesswire.com/portal/site/home/news/")
    register_url("data/www.globenewswire.com.html", "https://www.globenewswire.com")
    register_url("data/www.globenewswire.com.slash.newsroom.html", "https://www.globenewswire.com/NewsRoom")
    register_url("data/www.prnewswire.com.news.releases.html", "https://www.prnewswire.com/news-releases/"
                                                               "news-releases-list/?pagesize=50")
    register_url("data/www.prnewswire.com.news.releases.page.3.html",
                 "https://www.prnewswire.com/news-releases/news-releases-list/?page=3&pagesize=250")
    register_url("data/accesswire.newsroom.js", "https://www.accesswire.com/api/newsroom.ashx")
    register_url("data/accesswire.newsroom.new.json", "https://www.accesswire.com/users/api/newsroom?")
    register_url("data/accesswire.newsroom.new.public.json", "https://www.accesswire.com/users/api/public/newsroom", method=httpretty.POST)


def setup_httpretty():
    print("setup httpretty")
    httpretty.HTTPretty.allow_net_connect = False
    httpretty.enable()


def destroy_httpretty():
    # print "Tear down"
    httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
    httpretty.reset()  # reset HTTPretty state (clean up registered urls and request history)
    httpretty.HTTPretty.allow_net_connect = True


def list_tables():
    from pynamodb.connection import Connection
    conn = Connection() #host='http://localhost:8008')
    return conn.list_tables()['TableNames']


def teardown_module(module):
    print("teardown_module after everything in this file")
