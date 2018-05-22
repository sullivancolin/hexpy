# -*- coding: utf-8 -*-
"""Module for Realtime Results Api."""

import inspect
from .base import ROOT, handle_response, rate_limited
from .session import HexpySession
from typing import List, Dict, Any


class RealtimeAPI:
    """Class for working with RealtimeAPI.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession, RealtimeAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> realtime_client = RealtimeAPI(session)
    >>> realtime_client.list(team_id)
    >>> session.close()
    ```
    """

    TEMPLATE = ROOT + "realtime/monitor/"

    def __init__(self, session: HexpySession) -> None:
        self.session = session.session
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(self, name, rate_limited(fn))

    def cashtags(
        self, monitor_id: int, start: int = None, top: int = None
    ) -> Dict[str, Any]:
        """Get Cashtags associated to a Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
            start: Integer, specifies inclusive start date in epoch seconds.
            top: Integer, The top N cashtags to retrieve.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "cashtags",
                params={"id": monitor_id, "start": start, "top": top},
            )
        )

    def hashtags(
        self, monitor_id: int, start: int = None, top: int = None
    ) -> Dict[str, Any]:
        """Get Hashtags associated to a Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
            start: Integer, specifies inclusive start date in epoch seconds.
            top: Integer, The top N hashtags to retrieve.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "hashtags",
                params={"id": monitor_id, "start": start, "top": top},
            )
        )

    def list(self, team_id: int) -> Dict[str, Any]:
        """Get the Monitors which are in Proteus

        # Arguments
            team_id: Integer, The id of the team to which the listed monitors belong.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "list", params={"team_id": team_id})
        )

    def configure(self, monitor_id: int) -> Dict[str, Any]:
        """Configure the Realtime evaluators for the Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "configure", params={"id": monitor_id})
        )

    def enable(self, monitor_id: int) -> Dict[str, Any]:
        """Enable Realtime Data.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "enable", params={"id": monitor_id})
        )

    def disbale(self, monitor_id: int) -> Dict[str, Any]:
        """Disable Realtime Data.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "disable", params={"id": monitor_id})
        )

    def detail(self, monitor_id: int) -> Dict[str, Any]:
        """Get the Realtime evaluators details for the Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "details", params={"id": monitor_id})
        )

    def retweets(self, monitor_id: int) -> Dict[str, Any]:
        """Get the Realtime retweets for the Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "retweets", params={"id": monitor_id})
        )

    def social_guids(
        self,
        monitor_id: int,
        doc_type: str,
        start: int = None,
        received_after: int = None,
    ) -> Dict[str, Any]:
        """Get the Realtime social guids for the Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
            doc_type: String, Specifies the document type.
            start: Integer, specifies inclusive start date in epoch seconds.
            received_after: Integer, Specifies inclusive received after date in epoch seconds.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "socialguids",
                params={
                    "id": monitor_id,
                    "start": start,
                    "receivedafter": received_after,
                    "type": doc_type,
                },
            )
        )

    def tweets(self, monitor_id: int, start: int = None) -> Dict[str, Any]:
        """Get the Realtime tweets for the Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
            start: Integer, specifies inclusive start date in epoch seconds.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "tweets", params={"id": monitor_id, "start": start}
            )
        )

    def volume(
        self, monitor_id: int, start: int = None, doc_type: List = None
    ) -> Dict[str, Any]:
        """Get the Realtime volume for the Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
            start: Integer, specifies inclusive start date in epoch seconds.
            doc_type: List, specifies the document type to filter.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "volume",
                params={"id": monitor_id, "start": start, "type": doc_type},
            )
        )

    def volume_by_sentiment(
        self, monitor_id: int, start: int, doc_type: str
    ) -> Dict[str, Any]:
        """Get the Realtime volume by sentiment for the Monitor.

        # Arguments
            monitor_id: Integer, the id of the monitor being requested.
            start: Integer, specifies inclusive start date in epoch seconds.
            doc_type: String, specifies the document type to filter.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "volumebysentiment",
                params={"id": monitor_id, "start": start, "type": doc_type},
            )
        )
