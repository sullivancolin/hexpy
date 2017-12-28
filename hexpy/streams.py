# -*- coding: utf-8 -*-
"""Module for Realtime streams API."""

from .base import ROOT, response_handler
from .session import HexpySession
from requests.models import Response


class StreamsAPI(object):
    """Class for working with Realtime Streams API.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession, StreamsAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> streams_client = StreamsAPI(session)
    >>> streams_client.stream_list(team_id)
    >>> session.close()
    ```
    """

    TEMPLATE = ROOT + "stream/"

    def __init__(self, session: HexpySession) -> None:
        super(StreamsAPI, self).__init__()
        self.session = session.session

    @response_handler
    def posts(self, stream_id: int, count: int = 100) -> Response:
        """Return posts from a stream.

        # Arguments:
            stream_id: Integer, the id of the stream containing the posts, available via the stream list endpoint
            count: Integer, the count of posts to retrieve from the stream, max = 100
        """
        if count > 100:
            count = 100

        return self.session.get(
            self.TEMPLATE + "{stream_id}/posts".format(stream_id=stream_id),
            params={
                "count": count,
            })

    @response_handler
    def stream_list(self, team_id: int) -> Response:
        """List all available Realtime Streams for a team.

        # Arguments
            team_id: Integer the id of the team, available via the team list endpoint
        """
        return self.session.get(
            self.TEMPLATE + "list/", params={"teamid": team_id})
