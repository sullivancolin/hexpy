# -*- coding: utf-8 -*-
"""Moduel for interacting with analysis API"""

from .base import ROOT, response_handler


class AnalysisAPI(object):
    """Class for working with Crimson Hexagon Analysis API.

    # Example Usage

    ```python
    >>> from hexpy import HexpyAuthorization, AnalysisAPI
    >>> auth = HexpyAuthorization.load_auth_from_file()
    >>> analysis_client = AnalysisAPI(auth)
    >>> analysis_client.results(request_id)
    ```
    """

    TEMPLATE = ROOT + "results/"

    def __init__(self, authorization):
        super(AnalysisAPI, self).__init__()
        self.session = authorization.session

    @response_handler
    def analysis_request(self, data):
        """Submit a query task against 24 hours of social data.

        # Arguments
            data: Dictionary, query and filter parameters
        """
        return self.session.post(self.TEMPLATE, json=data)

    @response_handler
    def results(self, request_id):
        """Retrieve the status of the analysis request and the results.

        # Arguments
            request_id: Integer, the identifier given for the analysis, generated via the Analysis Request endpoints
        """
        return self.session.get(self.TEMPLATE + "{request_id}".format(
            request_id=request_id))
