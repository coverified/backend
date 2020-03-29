# /src/views/FeedView

from flask import Blueprint, request, json, Response
from dateutil.parser import parse

import datetime as dt

from src.models import FeedSchema, FeedDataModel

feed_api = Blueprint('feed_api', __name__)
feed_schema = FeedSchema()


@feed_api.route('/', methods=['GET'])
def feed_request():
    try:
        timestamp = parse(request.args.get("timestamp"), fuzzy=True)
        limit = int(request.args.get("limit"))
    except (ValueError, OverflowError) as e:
        return custom_response(str(e), 400)

    feed_elements = FeedDataModel.get_entries_of_last_hour(timestamp, limit)
    if not feed_elements:
        return custom_response([], 400)  # return empty list
    feed_data = [feed_schema.dump(element) for element in feed_elements]
    return custom_response(feed_data, 200)  # return data


@feed_api.after_request
def add_header(response):
    response.cache_control.max_age = 3600
    if 'Expires' not in response.headers:  # set expires date in iso format
        response.headers['Expires'] = dt.datetime.utcnow().isoformat()
    return response


def custom_response(res, status_code):
    """
    Convert the resulting data to a custom response including header data
    :param res: the response to be processed
    :param status_code: the status code
    :return: transformed custom response data
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
