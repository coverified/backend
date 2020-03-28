# /run.py
import os
import sys
from dotenv import load_dotenv, find_dotenv

from src.app import create_app
from src.rss.crawler import create_crawler

load_dotenv(find_dotenv())

env_name = os.getenv('FLASK_ENV')

if env_name is None:  # todo more sanity checks for the whole config
    sys.exit("Flask env not provided.")

# start the app
app = create_app(env_name)

# start the scheduler
# rss_crawler = create_crawler().start()

if __name__ == '__main__':
    port = os.getenv('API_PORT')
    # run backend app
    app.run(host='0.0.0.0', port=port, use_reloader=False)

    # run scheduler for rss feeds
