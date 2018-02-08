# -*- coding: utf-8 -*-
"""Moduel for interacting with analysis API"""

import inspect
from .base import ROOT, response_handler
from .session import HexpySession
from requests.models import Response
from typing import Dict, Any


class AnalysisAPI(object):
    """Class for working with Crimson Hexagon Analysis API.

    # Example Usage

    ```python
    >>> from hexpy import HexpySession, AnalysisAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> analysis_client = AnalysisAPI(session)
    >>> analysis_client.results(request_id)
    >>> session.close()
    ```
    """

    TEMPLATE = ROOT + "results"

    def __init__(self, session: HexpySession) -> None:
        super(AnalysisAPI, self).__init__()
        self.session = session.session
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(self, name, response_handler(fn))

    def analysis_request(self, data: Dict[str, Any]) -> Response:
        """Submit a query task against 24 hours of social data.

        # Arguments
            data: Dictionary, query and filter parameters
        """
        return self.session.post(self.TEMPLATE, json=data)

    def results(self, request_id: int) -> Response:
        """Retrieve the status of the analysis request and the results.

        # Arguments
            request_id: Integer, the identifier given for the analysis, generated via the Analysis Request endpoints
        """
        return self.session.get(self.TEMPLATE + "/{request_id}".format(
            request_id=request_id))
