# -*- coding: utf-8 -*-
"""Custom API request"""
from .base import ROOT, response_handler
from .session import HexpySession
from requests.models import Response
from typing import Any, Dict


class CustomAPI(object):
    """Class for creating a custom API.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession , CustomAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> custom_client = CustomAPI(session, "/some/endpoint/")
    >>> custom_client.get(url_params="<url_param1>/path", params={"query_string_param":some_value})
    >>> session.close()
    ```
    """

    def __init__(self, session: HexpySession, endpoint: str) -> None:
        super(CustomAPI, self).__init__()
        self.session = session.session
        self.TEMPLATE = ROOT + endpoint

    @response_handler
    def get(self, url_params: str, params: Dict[str, Any] = None) -> Response:
        """Send get request using URL parameters and query-string parameters."""
        return self.session.get(self.TEMPLATE + url_params, params=params)

    @response_handler
    def post(
            self,
            url_params: str,
            params: Dict[str, Any] = None,
            data: Dict[str, Any] = None, ) -> Response:
        """Send post request using URL parameters and query-string parameters, and json data"""
        return self.session.post(
            self.TEMPLATE + url_params, params=params, json=data)

    @response_handler
    def delete(self, url_params: str,
               params: Dict[str, Any] = None) -> Response:
        """Send delete request using URL parameters and query-string parameters."""
        return self.session.delete(self.TEMPLATE + url_params, params=params)
