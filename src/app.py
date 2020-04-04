# src/app.py
import json

import logging as log

from flask import Flask

from .config import app_config
from .crawler.RssCrawler import create_crawler
from .debug.SQLQueryDebugger import sql_debug
from .models import db

# import feed_api blueprint
from .views.FeedView import feed_api as feed_blueprint

# api limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import configparser


def create_app(env_name):
    """
    Create app
    """

    # app initialization
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    # defaults
    log_level = log.INFO

    # read config
    config = configparser.ConfigParser()
    config.read('cfg/config.cfg')

    # debug
    if app_config[env_name].DEBUG:
        app.after_request(sql_debug)  # debug sql queries
        log_level = log.DEBUG  # debug log enabled

    # configure logger
    log.basicConfig(format='[%(asctime)s] [%(module)s] [%(levelname)s] [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S:%f', level=log_level)

    # initializing db
    db.init_app(app)
    db.app = app

    # register the feed api blueprint
    app.register_blueprint(feed_blueprint, url_prefix='/api/v1/feed')

    # start the crawler
    keywords = json.loads(config.get("crawler", "keywords"))
    feeds = json.loads(config.get("crawler", "feeds"))
    create_crawler(keywords, feeds)

    # limit the number of api calls
    Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["20000 per day", "500 per hour"]
    )

    @app.route('/', methods=['GET'])
    def index():
        """
        main endpoint -> empty
        """
        return ''

    return app
