# src/app.py

from flask import Flask
from flask_restful import Api

from .config import app_config
from .models import db

# import feed_api blueprint
from .views.FeedView import feed_api as feed_blueprint


def create_app(env_name):
    """
    Create app
    """

    # app initialization
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    # initializing db
    db.init_app(app)

    # @feed_blueprint.route('/movie1/<page_num>')
    # def movie2(page_num=1):
    #     return str(page_num)

    app.register_blueprint(feed_blueprint, url_prefix='/api/v1/feed')


    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your part 2 endpoint is working'  # todo JH

    return app
