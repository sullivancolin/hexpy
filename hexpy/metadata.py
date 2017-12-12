# -*- coding: utf-8 -*-
"""Module for API Metadata"""

from .base import ROOT, response_handler


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

    def __init__(self, session):
        super(MetadataAPI, self).__init__()
        self.session = session.session

    @response_handler
    def team_list(self):
        """Return a list of teams accessible to the requesting user."""
        return self.session.get(self.TEMPLATE + "team/list")

    @response_handler
    def monitor_list(self, team_id):
        """Returns a list of monitors accessible to the requesting
        or selected user along with metadata related to those monitors.

        # Arguments
            team_id: integer id number for a team
        """
        return self.session.get(
            self.TEMPLATE + "monitor/list", params={"team": team_id})

    @response_handler
    def geography(self):
        """Return all the geographical locations that you may use to
        filter monitor results and to upload documents with location information.
        """
        return self.session.get(self.TEMPLATE + "geography/info/all")

    @response_handler
    def states(self, country):
        """Return all the states for a given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country code to filter states
        """
        return self.session.get(
            self.TEMPLATE + "geography/info/states",
            params={"country": country})

    @response_handler
    def cities(self, country):
        """Returns all the cities or urban areas defined in the given country that you may use to
        filter monitor results and to upload documents with location information.

        # Arguments
            country: country: country code  to filter states
        """
        return self.session.get(
            self.TEMPLATE + "geography/info/cities",
            params={"country": country})

    @response_handler
    def countries(self):
        """Returns all the countries that you may use to filter monitor results
        and to upload documents with location information.
        """
        return self.session.get(self.TEMPLATE + "geography/info/countries")
