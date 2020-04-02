# /src/views/CrawlerView
import time
import atexit

import feedparser
import lxml.html
import datetime as dt

from src.app import log

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.exc import OperationalError as SQOperationalError
from psycopg2 import OperationalError as PsyOperationalError

from src.models import FeedDataModel

keywords = []
feeds = []


def create_crawler(filter_words, feed_urls):
    log.info("Starting rss crawler...")
    # set the global vals
    global keywords
    keywords = filter_words

    global feeds
    feeds = feed_urls

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=crawl_and_persist_data, trigger="interval",
                      seconds=3600)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # crawl once on startup
    for job in scheduler.get_jobs():
        job.modify(next_run_time=(dt.datetime.utcnow() + dt.timedelta(minutes=2)))

    log.info("Rss crawler startup successful!")
    scheduler.start()


def crawl_and_persist_data():
    try:
        log.info("Collecting data from rss feeds...")
        rss_data_list = crawl_rss_data()
        log.info("Data from rss feeds collected.")
        log.info("Persisting collected data to database...")
        for feed_entry in rss_data_list:
            build_feed_data_and_persist(feed_entry)
    except (SQOperationalError, PsyOperationalError) as e:
        log.error("Persisting data from crawled feed failed with exception: " + str(e))
    log.info("Successfully persisted rss feed data to database!")


def build_feed_data_and_persist(feed_entry):
    timestamp = feed_entry.published  # todo parse
    title = feed_entry.title
    content = feed_entry.summary
    url = feed_entry.link

    data = {'timestamp': timestamp, 'title': title, 'content': content, 'url': url}

    feed_data = FeedDataModel(data)
    feed_data.persist_uniques()


def crawl_rss_data():
    return list(filter(lambda x: filter_keywords(filter_html(x.title)),
                       flatten([feedparser.parse(feed_url).entries for feed_url in feeds])))


def print_date_time():  # todo JH remove as this is debug method
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def filter_keywords(string):
    return bool(any(x in string.casefold() for x in keywords))


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
