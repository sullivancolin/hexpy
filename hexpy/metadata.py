# -*- coding: utf-8 -*-
"""Module for handling API Metadata"""

import requests
from .response import handle_response
from ratelimiter import RateLimiter

ONE_MINUTE = 60


class MetadataAPI(object):
    """docstring for MetadataAPI"""

    TEMPLATE = "https://api.crimsonhexagon.com/api/"

    def __init__(self, authorization):
        super(MetadataAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def team_list(self):
        return handle_response(
            requests.get(self.TEMPLATE + "team/list?auth={token}".format(
                token=self.authorization.token)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def monitor_list(self, team_id):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "monitor/list?auth={token}&team={team_id}".format(
                             token=self.authorization.token, team_id=team_id)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def geography(self):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "geography/info/all?auth={token}".format(
                             token=self.authorization.token)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def states(self, country):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "geography/info/states?auth={token}".format(
                             token=self.authorization.token, country=country)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def cities(self, country):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "geography/info/cities?auth={token}".format(
                             token=self.authorization.token, country=country)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def countries(self):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "geography/info/countries?auth={token}".format(
                             token=self.authorization.token)))
