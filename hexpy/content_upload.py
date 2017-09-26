# -*- coding: utf-8 -*-
"""Module for uploading custom content"""

import requests
from .response import handle_response
from ratelimiter import RateLimiter
from clint.textui import progress
ONE_MINUTE = 60


class ContentUploadAPI(object):
    """docstring for MetadataAPI"""

    TEMPLATE = "https://api.crimsonhexagon.com/api/content/upload"

    def __init__(self, authorization):
        super(ContentUploadAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def upload(self, data):
        return handle_response(
            requests.post(
                self.TEMPLATE,
                json={"items": data},
                params={"auth": self.authorization.token}))

    def batch_upload(self, data):
        assert (len(data) > 1000)
        for batch in progress.bar(
            [data[i:i + 1000] for i in range(0, len(data), 1000)]):
            self.upload(batch)
