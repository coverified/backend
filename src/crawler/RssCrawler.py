# /src/views/CrawlerView

import feedparser
import lxml.html

from src.app import log

from sqlalchemy.exc import OperationalError as SQOperationalError, ProgrammingError
from psycopg2 import OperationalError as PsyOperationalError

from src.models import FeedDataModel

import html

keywords = []
feeds = []


def create_crawler(filter_words, feed_urls):
    log.info("Configure rss crawler...")
    # set the global vals
    global keywords
    keywords = filter_words

    global feeds
    feeds = feed_urls

    log.info("Successfully configured rss crawler!")


def crawl_and_persist_data():
    success = bool(False)
    try:
        log.info("Collecting data from rss feeds...")
        rss_data_list = crawl_rss_data()
        log.info("Collected " + str(len(rss_data_list)) + " elements.")
        log.info("Persisting collected data to database...")
        for feed_entry in rss_data_list:
            build_feed_data_and_persist(feed_entry)
        success = bool(True)
    except (SQOperationalError, PsyOperationalError, ProgrammingError) as e:
        log.error("Persisting data from crawled feed failed with exception: " + str(e))

    if success:
        log.info("Successfully persisted rss feed data to database!")


def build_feed_data_and_persist(feed_entry):
    timestamp = feed_entry.published
    title = clean_string(feed_entry.title)
    content = clean_string(feed_entry.summary)
    url = feed_entry.link

    data = {'timestamp': timestamp, 'title': title, 'content': content, 'url': url}

    feed_data = FeedDataModel(data)
    feed_data.persist_uniques()


def crawl_rss_data():
    return list(filter(lambda x: filter_keywords(clean_string(filter_html(x.title + x.summary))),
                       flatten([feedparser.parse(feed_url).entries for feed_url in feeds])))


def filter_keywords(string):
    return bool(any(x in string.casefold() for x in keywords))


def clean_string(string):
    # we don't want soft hyphen in the db
    soft_hyphen_html = "&#173;"
    # we don't want line breaks in the db
    return html.unescape(string.replace(soft_hyphen_html, "").replace("\n", " "))


def filter_html(string):
    if not string:
        return string
    return lxml.html.fromstring(string).text_content()


def flatten(list):
    flat_list = []
    for sublist in list:
        for item in sublist:
            flat_list.append(item)
    return flat_list
