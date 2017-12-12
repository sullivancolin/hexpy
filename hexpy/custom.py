# -*- coding: utf-8 -*-
"""Custom API request"""
from .base import ROOT, response_handler


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

    def __init__(self, session, endpoint):
        super(CustomAPI, self).__init__()
        self.session = session.session
        self.TEMPLATE = ROOT + endpoint

    @response_handler
    def get(self, url_params, params=None):
        """Send get request using URL parameters and query-string parameters."""
        return self.session.get(self.TEMPLATE + url_params, params=params)

    @response_handler
    def post(self, url_params, params=None, data=None):
        """Send post request using URL parameters and query-string parameters, and json data"""
        return self.session.post(
            self.TEMPLATE + url_params, params=params, json=data)

    @response_handler
    def delete(self, url_params, params=None):
        """Send delete request using URL parameters and query-string parameters."""
        return self.session.delete(self.TEMPLATE + url_params, params=None)
