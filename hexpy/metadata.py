# -*- coding: utf-8 -*-
"""Module for API Metadata"""

import requests
from .response import handle_response
from ratelimiter import RateLimiter
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class MetadataAPI(object):
    """Class for working with Crimson Hexagon account and analysis metadata.

    # Example usage.

    ```python
    >>> from hexpy import CrimsonAuthorization, MetadataAPI
    >>> auth = CrimsonAuthorization.load_auth_from_file()
    >>> metadata_client = MetadataAPI(auth)
    >>> metadata_client.team_list()
    ```
    """

    TEMPLATE = ROOT

    def __init__(self, authorization):
        super(MetadataAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def team_list(self):
        """Return a list of teams accessible to the requesting user."""
        return handle_response(
            requests.get(self.TEMPLATE + "team/list",
                         params={"auth": self.authorization.token}))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def monitor_list(self, team_id):
        """Returns a list of monitors accessible to the requesting
        or selected user along with metadata related to those monitors.

        # Arguments
            team_id: integer id number for a team
        """
        return handle_response(
            requests.get(self.TEMPLATE + "monitor/list",
                         params={
                             "auth": self.authorization.token,
                             "team": team_id
                         }))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def geography(self):
        """Return all the geographical locations that you may use to
        filter monitor results and to upload documents with location information.
        """
        return handle_response(
            requests.get(self.TEMPLATE + "geography/info/all",
                         params={
                             "auth": self.authorization.token
                         }))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def states(self, country):
        """Return all the states for a given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country code to filter states
        """
        return handle_response(
            requests.get(self.TEMPLATE + "geography/info/states",
                         params={
                             "auth": self.authorization.token,
                             "country": country
                         }))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def cities(self, country):
        """Returns all the cities or urban areas defined in the given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country: country code  to filter states
        """
        return handle_response(
            requests.get(self.TEMPLATE + "geography/info/cities",
                         params={
                             "auth": self.authorization.token,
                             "country": country
                         }))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def countries(self):
        """Returns all the countries that you may use to filter monitor results
        and to upload documents with location information.
        """
        return handle_response(
            requests.get(self.TEMPLATE + "geography/info/countries",
                         params={
                             "auth": self.authorization.token
                         }))
