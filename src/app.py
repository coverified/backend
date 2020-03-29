# src/app.py

from flask import Flask

from .config import app_config
from .debug.sql_query_debugger import sql_debug
from .models import db

# import feed_api blueprint
from .views.FeedView import feed_api as feed_blueprint

# api limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_app(env_name):
    """
    Create app
    """

    # app initialization
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])

    # debug
    if app_config[env_name].DEBUG:
        app.after_request(sql_debug)

    # initializing db
    db.init_app(app)

    # register the feed api blueprint
    app.register_blueprint(feed_blueprint, url_prefix='/api/v1/feed')

    # limit the number of api calls
    Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["20000 per day", "500 per hour"]
    )

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your part 2 endpoint is working'  # todo JH

    return app
