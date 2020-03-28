# src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy

# init the db
db = SQLAlchemy()

from .FeedDataModel import FeedDataModel, FeedSchema
