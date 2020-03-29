# src/models/FeedDataModel.py
from . import db
from marshmallow import fields, Schema
import datetime as dt


class FeedDataModel(db.Model):
    """
    RSS Feed Data Model
    """

    # table name
    __tablename__ = 'feed_data'

    tid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

    # class constructor

    def __init__(self, data):
        """
        FeedDataModel class constructor
        """

        self.timestamp = data.get('timestamp')
        self.title = data.get('title')
        self.content = data.get('content')
        self.url = data.get('url')
        self.created_at = dt.datetime.utcnow()
        self.modified_at = dt.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr(self):
        return '<id {}>'.format(self.id)

    def persist_uniques(self):
        # persists only if an element with this title does not exist yet in the database
        exist = FeedDataModel.query.filter(FeedDataModel.title == self.title).scalar() is not None
        if not exist:
            self.save()

    @staticmethod
    def get_entries(start_date, end_date, limit):
        return FeedDataModel.query.filter(
            FeedDataModel.timestamp.between(start_date, end_date)).limit(limit).all()


class FeedSchema(Schema):
    tid = fields.Int(dump_only=True)
    timestamp = fields.DateTime(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
