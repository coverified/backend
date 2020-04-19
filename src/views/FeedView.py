# /src/views/FeedView

import os
from flask import Blueprint, request, json, Response
from dateutil.parser import parse

import datetime as dt

from sqlalchemy.exc import OperationalError

from src.models import FeedSchema, FeedDataModel

feed_api = Blueprint('feed_api', __name__)
feed_schema = FeedSchema()


@feed_api.route('/', methods=['GET'])
def feed_request():
    try:
        start_date = parse(request.args.get("start"), fuzzy=True, dayfirst=True)
        end_date = parse(request.args.get("end"), fuzzy=True, dayfirst=True)
        limit = int(request.args.get("limit"))
    except (ValueError, OverflowError, TypeError) as e:
        return custom_response(str(e), 400)

    try:
        feed_elements = FeedDataModel.get_entries(start_date, end_date, limit)
    except OperationalError as e:
        return custom_response(str(e), 400)

    if not feed_elements:
        return custom_response([], 400)  # return empty list
    feed_data = [feed_schema.dump(element) for element in feed_elements]
    return custom_response(feed_data, 200)  # return data


@feed_api.route('/latest', methods=['GET'])
def get_latest():
    limit = request.args.get('limit', None)
    offset = request.args.get('offset', None)
    try:
        limit = int(limit)
        offset = int(offset)
        feed_elements = FeedDataModel.get_latest(limit, offset)
    except OperationalError as e:
        return custom_response(str(e), 400)
    except (ValueError, TypeError):
        return custom_response(
            "Cannot parse provided values for limit=" + str(limit) + " and offset=" + str(offset) +
            ". Please ensure that both values are of type 'int'.", 400)

    if not feed_elements:
        return custom_response([], 400)

    feed_data = [feed_schema.dump(element) for element in feed_elements]
    return custom_response(feed_data, 200)


@feed_api.after_request
def add_header(response):
    response.cache_control.max_age = 3600
    response.access_control_allow_origin = "*"
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
