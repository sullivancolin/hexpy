# -*- coding: utf-8 -*-
"""Module for API Metadata"""

import requests
from .response import handle_response
from ratelimiter import RateLimiter
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class MetadataAPI(object):
    """docstring for MetadataAPI"""

    TEMPLATE = ROOT

    def __init__(self, authorization):
        super(MetadataAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def team_list(self):
        return handle_response(
            requests.get(self.TEMPLATE + "team/list?auth={token}".format(
                token=self.authorization.token)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def monitor_list(self, team_id):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "monitor/list?auth={token}&team={team_id}".format(
                             token=self.authorization.token, team_id=team_id)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def geography(self):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "geography/info/all?auth={token}".format(
                             token=self.authorization.token)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def states(self, country):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "geography/info/states?auth={token}&country={country}".format(
                    token=self.authorization.token, country=country)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def cities(self, country):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "geography/info/cities?auth={token}&country={country}".format(
                    token=self.authorization.token, country=country)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def countries(self):
        return handle_response(
            requests.get(self.TEMPLATE +
                         "geography/info/countries?auth={token}".format(
                             token=self.authorization.token)))
