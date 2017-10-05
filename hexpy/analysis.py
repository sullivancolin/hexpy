# -*- coding: utf-8 -*-
"""Moduel for interacting with analysis API"""

import requests
from .response import handle_response
from ratelimiter import RateLimiter
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class AnalysisAPI(object):
    """Class for working with Crimson Hexagon Analysis API.

    # Example Usage

    ```python
    >>> from hexpy import CrimsonAuthorization, AnalysisAPI
    >>> auth = CrimsonAuthorization.load_auth_from_file()
    >>> analysis_client = AnalysisAPI(auth)
    >>> analysis_client.results(request_id)
    ```
    """

    TEMPLATE = ROOT + "results/"

    def __init__(self, authorization):
        super(AnalysisAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def analysis_request(self, data):
        """Submit a query task against 24 hours of social data.

        # Arguments
            data: Dictionary, query and filter parameters
        """
        return handle_response(
            requests.post(self.TEMPLATE),
            json=data,
            params={"auth": self.authorization.token})

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def results(self, request_id):
        """Retrieve the status of the analysis request and the results.

        # Arguments
            request_id: Integer, the identifier given for the analysis, generated via the Analysis Request endpoints
        """
        return handle_response(
            requests.get(self.TEMPLATE + "{request_id}".format(request_id),
                         params={
                             "auth": self.authorization.token
                         }))
