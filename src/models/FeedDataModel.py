# src/models/FeedDataModel.py
from . import db
from marshmallow import fields, Schema
import datetime


class FeedDataModel(db.Model):
    """
    RSS Feed Data Model
    """

    # table name
    __tablename__ = 'feed_data'

    tid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(128), unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

    # class constructor

    def __init__(self, data):
        """
        FeedDataModel class constructor
        """

        self.tid = data.get('tid')
        self.timestamp = data.get('timestamp')
        self.title = data.get('title')
        self.content = data.get('content')
        self.url = data.get('url')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def get_entry(tid):
        return FeedDataModel.query.get(tid)


class FeedSchema(Schema):
    tid = fields.Int(dump_only=True)
    timestamp = fields.DateTime(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
