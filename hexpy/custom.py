# -*- coding: utf-8 -*-
"""Custom API request"""

import inspect
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
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(self, name, response_handler(fn))

    def get(self, url_params: str = "",
            params: Dict[str, Any] = None) -> Response:
        """Send get request using URL parameters and query-string parameters.

        # Arguments
            url_params: String, url params and endpoints concatenated.
            params: Dict, querystring params.

        """
        return self.session.get(self.TEMPLATE + url_params, params=params)

    def post(
            self,
            url_params: str = "",
            params: Dict[str, Any] = None,
            data: Dict[str, Any] = None, ) -> Response:
        """Send post request using URL parameters and query-string parameters, and json data.

        # Arguments
            url_params: String, url params and endpoints concatenated.
            params: Dict, querystring params.
            data: Dict, json data to post.
        """
        return self.session.post(
            self.TEMPLATE + url_params, params=params, json=data)

    def delete(self, url_params: str = "",
               params: Dict[str, Any] = None) -> Response:
        """Send delete request using URL parameters and query-string parameters.

        # Arguments
            url_params: String, url params and endpoints concatenated.
            params: Dict, querystring params.
        """
        return self.session.delete(self.TEMPLATE + url_params, params=params)
