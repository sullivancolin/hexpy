"""Module for Activity Reports Api."""

import inspect
from .base import handle_response, rate_limited
from .session import HexpySession
from typing import Dict, Any


class ActivityAPI:
    """Class for working with Activity Reports API.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession, ActivityAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> activity_client = ActivityAPI(session)
    >>> activity_client.monitor_creation(team_id)
    ```
    """

    def __init__(self, session: HexpySession) -> None:
        self.session = session.session
        self.TEMPLATE = session.ROOT + "report/"
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(
                    self, name, rate_limited(fn, session.MAX_CALLS, session.ONE_MINUTE)
                )

    def monitor_creation(self, organization_id: int) -> Dict[str, Any]:
        """Get Monitor Creation Report for all teams within an organization and how many monitors were created during a given time period.

        # Arguments
            organiztion_id: Integer, the id of the organization being requested.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "monitorCreation", params={"id": organization_id}
            )
        )

    def social_sites(self, organization_id: int) -> Dict[str, Any]:
        """Get Social Site Report and associated usernames for Teams within an Organization.

        # Arguments
            organiztion_id: Integer, the id of the organization being requested.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "socialSites", params={"id": organization_id}
            )
        )

    def user_activity(self, organization_id: int) -> Dict[str, Any]:
        """Get a list of users indicating when they last logged into the platform, the last monitor they created, and the last monitor they viewed.

        # Arguments
            organiztion_id: Integer, the id of the organization being requested.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "userActivity", params={"id": organization_id}
            )
        )

    def user_invitations(self, organization_id: int) -> Dict[str, Any]:
        """Get a list of users within an Organization and which Team(s) they were invited to.

        # Arguments
            organiztion_id: Integer, the id of the organization being requested.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "userInvitations", params={"id": organization_id}
            )
        )
