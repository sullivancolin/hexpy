# -*- coding: utf-8 -*-
"""Module for real time streams API."""

import requests
from .response import handle_response
from ratelimiter import RateLimiter

ONE_MINUTE = 60


class StreamsAPI(object):
    """docstring for StreamsAPI"""

    TEMPLATE = "https://api.crimsonhexagon.com/api/stream/"

    def __init__(self, authorization):
        super(StreamsAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def posts(self, stream_id, count=100):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "{stream_id}/posts?count={count}".format(
                             stream_id=stream_id, count=count)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def stream_list(self, team_id):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "list/?auth={token}&teamid={team_id}".format(
                             token=self.authorization.token, team_id=team_id)))
