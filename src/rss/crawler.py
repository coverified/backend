# src/rss/crawler.pys

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


def create_crawler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)  # todo JH interval as config param

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    return scheduler


def print_date_time():  # todo JH remove as this is debug method
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())
