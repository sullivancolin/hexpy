# -*- coding: utf-8 -*-
"""Module for Streams API."""

import inspect
from typing import Dict, Any
from .base import ROOT, handle_response, rate_limited
from .session import HexpySession


class StreamsAPI:
    """Class for working with Streams API.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession, StreamsAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> streams_client = StreamsAPI(session)
    >>> streams_client.stream_list(team_id)
    >>> session.close()
    ```
    """

    TEMPLATE = ROOT + "stream"

    def __init__(self, session: HexpySession) -> None:
        self.session = session.session
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(self, name, rate_limited(fn))

    def posts(self, stream_id: int, count: int = 100) -> Dict[str, Any]:
        """Return posts from a stream.

        # Arguments:
            stream_id: Integer, the id of the stream containing the posts
            count: Integer, the count of posts to retrieve from the stream, max = 100.
        """
        if count > 100:
            count = 100

        return handle_response(
            self.session.get(
                self.TEMPLATE + f"/{stream_id}/posts", params={"count": count}
            )
        )

    def stream_list(self, team_id: int) -> Dict[str, Any]:
        """List all available streams for a team.

        # Arguments
            team_id: Integer, the id of the team.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "/list/", params={"teamid": team_id})
        )

    def create_stream(self, team_id: int, name: str) -> Dict[str, Any]:
        """Create new stream for a team. System Admin Only.

        # Arguments
            team_id: Integer, the id of the team to associate created stream with.
            name: String, the name to associate with the newly created stream.
        """
        return handle_response(
            self.session.post(self.TEMPLATE, json={"teamid": team_id, "name": name})
        )

    def delete_stream(self, stream_id: int) -> Dict[str, Any]:
        """Delete a stream. System Admin Only.

        # Arguments
            stream_id: Integer, the id of the stream to be deleted.
        """
        return handle_response(self.session.delete(self.TEMPLATE + f"/{stream_id}"))

    def add_monitor_to_stream(self, stream_id: int, monitor_id: int) -> Dict[str, Any]:
        """Associate a monitor with a stream. System Admin Only.

        # Arguments
            stream_id: Integer, the id of stream to be modified.
            monitor_id: Integer, the id to be associated with the stream.
        """
        return handle_response(
            self.session.post(self.TEMPLATE + f"/{stream_id}/monitor/{monitor_id}")
        )

    def remove_monitor_from_stream(
        self, stream_id: int, monitor_id: int
    ) -> Dict[str, Any]:
        """Remove association between monitor and stream.  System Admin Only.

        # Arguments
            stream_id: Integer, the id of stream to be updated.
            monitor_id: Integer, the id to be removed from the stream.
        """
        return handle_response(
            self.session.delete(self.TEMPLATE + f"/{stream_id}/monitor/{monitor_id}")
        )

    def update_stream(self, stream_id: int, name: str) -> Dict[str, Any]:
        """Update name of stream. System Admin Only.

        # Arguments
            stream_id: Integer, the id of stream to be updated.
            name: String, the new name to be associated with the stream.
        """
        return handle_response(
            self.session.post(self.TEMPLATE + f"/{stream_id}", json={"name": name})
        )
