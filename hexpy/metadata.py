# -*- coding: utf-8 -*-
"""Module for API Metadata"""

import inspect
from typing import Dict, Any
from .base import ROOT, handle_response, rate_limited
from .session import HexpySession


class MetadataAPI:
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
        self.session = session.session
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(self, name, rate_limited(fn))

    def team_list(self) -> Dict[str, Any]:
        """Return a list of teams accessible to the requesting user."""
        return handle_response(self.session.get(self.TEMPLATE + "team/list"))

    def monitor_list(self, team_id: int) -> Dict[str, Any]:
        """Return a list of monitors accessible to the requesting
        or selected user along with metadata related to those monitors.

        # Arguments
            team_id: integer id number for a team
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "monitor/list", params={"team": team_id})
        )

    def geography(self) -> Dict[str, Any]:
        """Return all the geographical locations that you may use to
        filter monitor results and to upload documents with location information.
        """
        return handle_response(self.session.get(self.TEMPLATE + "geography/info/all"))

    def states(self, country: str) -> Dict[str, Any]:
        """Return all the states for a given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country code to filter states
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "geography/info/states", params={"country": country}
            )
        )

    def cities(self, country: str) -> Dict[str, Any]:
        """Return all the cities or urban areas defined in the given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country: country code  to filter states
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "geography/info/cities", params={"country": country}
            )
        )

    def countries(self) -> Dict[str, Any]:
        """Return all the countries that you may use to filter monitor results
        and to upload documents with location information.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "geography/info/countries")
        )

    def api_documentation(self) -> Dict[str, Any]:
        """Return latest JSON version of Crimson Hexagon API endpoint documentation."""
        return handle_response(self.session.get(self.TEMPLATE + "documentation"))
