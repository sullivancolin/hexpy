import requests
from .response import handle_response
from ratelimiter import RateLimiter

ONE_MINUTE = 60


class AnalysisAPI(object):
    """docstring for AnalysisAPI"""

    TEMPLATE = "https://api.crimsonhexagon.com/api/results/"

    def __init__(self, authorization):
        super(AnalysisAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def analysis_request(self, data):
        return handle_response(
            requests.post(self.TEMPLATE),
            json=data,
            params={"auth": self.authorization.token})

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def results(self, request_id):
        return handle_response(
            requests.get(self.TEMPLATE + "{request_id}?auth={token}".format(
                token=self.authorization.token, request_id=request_id)))
