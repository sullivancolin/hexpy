# -*- coding: utf-8 -*-
"""Module for Realtime streams API."""

import requests
from .response import handle_response
from ratelimiter import RateLimiter
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class StreamsAPI(object):
    """Class for working with Realtime Streams API."""

    TEMPLATE = ROOT + "stream/"

    def __init__(self, authorization):
        super(StreamsAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def posts(self, stream_id, count=100):
        """Return posts from a stream.

        # Arguments:
            stream_id: Integer, the id of the stream containing the posts, available via the stream list endpoint
            count: Integer, the count of posts to retrieve from the stream, max = 100
        """
        return handle_response(
            requests.get(self.TEMPLATE +
                         "{stream_id}/posts?count={count}".format(
                             stream_id=stream_id, count=count)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def stream_list(self, team_id):
        """List all available Realtime Streams for a team.

        # Arguments
            team_id: Integer the id of the team, available via the team list endpoint
        """
        return handle_response(
            requests.get(self.TEMPLATE +
                         "list/?auth={token}&teamid={team_id}".format(
                             token=self.authorization.token, team_id=team_id)))
