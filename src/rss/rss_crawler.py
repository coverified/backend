# src/rss/crawler.pys

import time
import atexit

import feedparser
import lxml.html

from apscheduler.schedulers.background import BackgroundScheduler

keywords = ('corona', 'covid', 'sars-cov', 'sars-cov', 'sars-cov', 'sars-cov', 'epidemic')  # todo config value
feeds = ('https://www.bundesregierung.de/service/rss/breg-de/1151244/feed.xml',  # todo config value
         'https://www.bundesgesundheitsministerium.de/rss.html',
         'https://www.rki.de/SiteGlobals/Functions/RSSFeed/RSSGenerator_nCoV.xml',
         'https://www.charite.de/service/pressemitteilung/feed/pressefeed/rss2feed.xml',
         'https://www.hopkinsmedicine.org/news/media/releases?format=rss'
         )


def create_crawler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=crawl_rss_data, trigger="interval", seconds=2)  # todo JH interval as config param

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    return scheduler


def crawl_and_persist_data():
    rss_data_list = crawl_rss_data()


def crawl_rss_data():
    return list(filter(lambda x: filter_keywords(filter_html(x.title)),
                       flatten([feedparser.parse(feed_url).entries for feed_url in feeds])))

    # print(len(coVidEntries))
    #
    # for entry in coVidEntries:
    #     print("\n")
    #     print(entry.title)
    # print("************")
    # print(entry.published)
    # print("#########")
    # print(entry.summary)
    # print("------News Link--------")
    # print(entry.link)


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
