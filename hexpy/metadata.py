# -*- coding: utf-8 -*-
"""Module for API Metadata"""

import inspect
from .base import ROOT, response_handler
from .session import HexpySession
from requests.models import Response


class MetadataAPI(object):
    """Class for working with Crimson Hexagon account and analysis metadata.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession, MetadataAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> metadata_client = MetadataAPI(session)
    >>> metadata_client.team_list()
    >>> session.close()
    ```
    """

    TEMPLATE = ROOT

    def __init__(self, session: HexpySession) -> None:
        super(MetadataAPI, self).__init__()
        self.session = session.session
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(self, name, response_handler(fn))

    def team_list(self) -> Response:
        """Return a list of teams accessible to the requesting user."""
        return self.session.get(self.TEMPLATE + "team/list")

    def monitor_list(self, team_id: int) -> Response:
        """Return a list of monitors accessible to the requesting
        or selected user along with metadata related to those monitors.

        # Arguments
            team_id: integer id number for a team
        """
        return self.session.get(
            self.TEMPLATE + "monitor/list", params={"team": team_id})

    def geography(self) -> Response:
        """Return all the geographical locations that you may use to
        filter monitor results and to upload documents with location information.
        """
        return self.session.get(self.TEMPLATE + "geography/info/all")

    def states(self, country: str) -> Response:
        """Return all the states for a given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country code to filter states
        """
        return self.session.get(
            self.TEMPLATE + "geography/info/states",
            params={"country": country})

    def cities(self, country: str) -> Response:
        """Return all the cities or urban areas defined in the given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country: country code  to filter states
        """
        return self.session.get(
            self.TEMPLATE + "geography/info/cities",
            params={"country": country})

    def countries(self) -> Response:
        """Return all the countries that you may use to filter monitor results
        and to upload documents with location information.
        """
        return self.session.get(self.TEMPLATE + "geography/info/countries")

    def api_documentation(self) -> Response:
        """Return latest version of API endpoint documentation."""
        return self.session.get(self.TEMPLATE + "documentation")
