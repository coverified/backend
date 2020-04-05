# /src/views/CrawlerView

import os
from ..crawler.RssCrawler import crawl_and_persist_data

from flask import Blueprint, json, Response

crawler_api = Blueprint('crawler_api', __name__)

# crawler api uuid token
crawler_token = os.getenv('CRAWLER_TOKEN')


@crawler_api.route('/run/<uuid>', methods=['POST'])
def execute_crawler(uuid):
    if uuid != crawler_token:
        return custom_response("Invalid access token provided!", 400)

    crawl_and_persist_data()
    return custom_response("Crawled and persisted rss feed data!", 200)


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
