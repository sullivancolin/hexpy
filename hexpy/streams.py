# -*- coding: utf-8 -*-
"""Module for Streams API."""

from .base import ROOT, response_handler
from .session import HexpySession
from requests.models import Response


class StreamsAPI(object):
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
        super(StreamsAPI, self).__init__()
        self.session = session.session

    @response_handler
    def posts(self, stream_id: int, count: int = 100) -> Response:
        """Return posts from a stream.

        # Arguments:
            stream_id: Integer, the id of the stream containing the posts
            count: Integer, the count of posts to retrieve from the stream, max = 100.
        """
        if count > 100:
            count = 100

        return self.session.get(
            self.TEMPLATE + "/{stream_id}/posts".format(stream_id=stream_id),
            params={
                "count": count,
            })

    @response_handler
    def stream_list(self, team_id: int) -> Response:
        """List all available streams for a team.

        # Arguments
            team_id: Integer, the id of the team.
        """
        return self.session.get(
            self.TEMPLATE + "/list/", params={"teamid": team_id})

    @response_handler
    def create_stream(self, team_id: int, name: str) -> Response:
        """Create new stream for a team. System Admin Only.

        # Arguments
            team_id: Integer, the id of the team to associate created stream with.
            name: String, the name to associate with the newly created stream.
        """
        return self.session.post(
            self.TEMPLATE, json={"teamid": team_id,
                                 "name": name})

    @response_handler
    def delete_stream(self, stream_id: int) -> Response:
        """Delete a stream. System Admin Only.

        # Arguments
            stream_id: Integer, the id of the stream to be deleted.
        """
        return self.session.delete(self.TEMPLATE + "/{stream_id}".format(
            stream_id=stream_id))

    @response_handler
    def add_monitor_to_stream(self, stream_id: int,
                              monitor_id: int) -> Response:
        """Associate a monitor with a stream. System Admin Only.

        # Arguments
            stream_id: Integer, the id of stream to be modified.
            monitor_id: Integer, the id to be associated with the stream.
        """
        return self.session.post(
            self.TEMPLATE + "/{stream_id}/monitor/{monitor_id}".format(
                stream_id=stream_id, monitor_id=monitor_id))

    @response_handler
    def remove_monitor_from_stream(self, stream_id: int,
                                   monitor_id: int) -> Response:
        """Remove association between monitor and stream.  System Admin Only.

        # Arguments
            stream_id: Integer, the id of stream to be updated.
            monitor_id: Integer, the id to be removed from the stream.
        """
        return self.session.delete(
            self.TEMPLATE + "/{stream_id}/monitor/{monitor_id}".format(
                stream_id=stream_id, monitor_id=monitor_id))

    @response_handler
    def update_stream(self, stream_id: int, name: str) -> Response:
        """Update name of stream. System Admin Only.

        # Arguments
            stream_id: Integer, the id of stream to be updated.
            name: String, the new name to be associated with the stream.
        """
        return self.session.post(
            self.TEMPLATE + "/{stream_id}".format(stream_id=stream_id),
            json={"name": name})