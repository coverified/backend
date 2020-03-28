# /src/views/FeedView

from flask import Blueprint, request, jsonify, Response, url_for

from src.models import FeedSchema, FeedDataModel

feed_api = Blueprint('feed_api', __name__)
feed_schema = FeedSchema()


# @feed_api.route('/<int:tid>', methods=['GET'])
# def fetch_entry(tid):
#     """
#     Get a single feed entry based on its table id
#     :param tid: the table id for the entry
#     :return: the found entry as json string or an error string
#     """
#     feed = FeedDataModel.get_entry(tid)
#     if not feed:
#         return custom_response("", 400)
#     feed_data = feed_schema.dumps(feed)
#     return custom_response(feed_data, 200)

@feed_api.route('/', methods=['GET'])
def test():
    try:
        timestamp = request.args.get("timestamp")  # todo parse
        limit = request.args.get("limit")  # todo parse
    except ValueError:
        return "", 400  # todo check that all exceptions are catched
    #     feed = FeedDataModel.get_entry(tid)
    #     if not feed:
    #         return custom_response("", 400)
    #     feed_data = feed_schema.dumps(feed)
    #     return custom_response(feed_data, 200)
    return "works", 200


def custom_response(res, status_code):
    """
    Convert the resulting data to a custom response including header data
    :param res: the response to be processed
    :param status_code: the status code
    :return: transformed custom response data
    """
    return Response(
        mimetype="application/json",
        response=res,
        status=status_code
    )
