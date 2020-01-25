"""Module for interacting with analysis API"""

import inspect

from .base import JSONDict, handle_response, rate_limited
from .models import AnalysisRequest
from .session import HexpySession


class AnalysisAPI:
    """Class for working with Crimson Hexagon Analysis API.

    # Example Usage

    ```python
    >>> from hexpy import HexpySession, AnalysisAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> analysis_client = AnalysisAPI(session)
    >>> analysis_client.results(request_id)
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

    def analysis_request(self, request: AnalysisRequest) -> JSONDict:
        """Submit a query task against 24 hours of social data.

        # Arguments
            request: validated AnalysisRequest.

        Example Request
        ```python
        request_dict = {
            "analysis": [
                "volume",
                "sentiment",
                "emotion",
                "affinity",
                "gender",
                "age",
                "location",
                "source",
                "reach"
            ],
            "keywords": "iPhone",
            "languages": {
                "type": "include",
                "values": [
                "EN"
                ]
            },
            "gender": {
                    "type": "include",
                    "values": ["M"]
            },
            "locations": {
                "type": "exclude",
                "values": [
                    "JPN"
                ]
            },
            "sources": [
                "TWITTER",
                "TUMBLR",
                "INSTAGRAM",
                "BLOGS",
                "REVIEWS",
                "GOOGLE_PLUS",
                "NEWS",
                "YOUTUBE",
                "FORUMS"
            ],
            "startDate": "2016-09-20T00:00:00",
            "endDate": "2016-09-21T00:00:00",
            "timezone": "America/New_York",
            "requestUsage": True
        }
        request = AnalysisRequest(**request_dict)
        ```

        """
        return handle_response(self.session.post(self.TEMPLATE, json=request))

    def results(self, request_id: int) -> JSONDict:
        """Retrieve the status of the analysis request and the results.

        # Arguments
            request_id: Integer, the identifier given for the analysis, generated via the Analysis Request endpoints
        """
        return handle_response(self.session.get(self.TEMPLATE + f"/{request_id}"))

    def image_analysis(self, url: str) -> JSONDict:
        """Get object, scene, activity predictions for image from public url.

        # Arguments
            url: String, the url of the image to analyze
        """

        return handle_response(
            self.session.get(
                self.TEMPLATE.split("results")[0] + "imageanalysis", params={"url": url}
            )
        )
