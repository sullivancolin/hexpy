"""Module for interacting with analysis API"""

import inspect
from .base import handle_response, rate_limited
from .session import HexpySession
from typing import Dict, Any


class AnalysisAPI:
    """Class for working with Crimson Hexagon Analysis API.

    # Example Usage

    ```python
    >>> from hexpy import HexpySession, AnalysisAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> analysis_client = AnalysisAPI(session)
    >>> analysis_client.results(request_id)
    >>> session.close()
    ```
    """

    def __init__(self, session: HexpySession) -> None:
        self.session = session.session
        self.TEMPLATE = session.ROOT + "results"
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["__init__"]:
                setattr(
                    self, name, rate_limited(fn, session.MAX_CALLS, session.ONE_MINUTE)
                )

    def analysis_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a query task against 24 hours of social data.

        # Arguments
            data: Dictionary, query and filter parameters
        """
        return handle_response(self.session.post(self.TEMPLATE, json=data))

    def results(self, request_id: int) -> Dict[str, Any]:
        """Retrieve the status of the analysis request and the results.

        # Arguments
            request_id: Integer, the identifier given for the analysis, generated via the Analysis Request endpoints
        """
        return handle_response(self.session.get(self.TEMPLATE + f"/{request_id}"))

    def image_analysis(self, url: str) -> Dict[str, Any]:
        """Get object, scene, activity predictions for image from public url.

        # Arguments
            url: String, the url of the image to analyze
        """

        return handle_response(
            self.session.get(
                self.TEMPLATE.split("results")[0] + "imageanalysis", params={"url": url}
            )
        )
