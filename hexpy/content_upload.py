# -*- coding: utf-8 -*-
"""Module for uploading custom content"""

import requests
from ratelimiter import RateLimiter
from clint.textui import progress
from .response import handle_response
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class ContentUploadAPI(object):
    """docstring for MetadataAPI."""

    TEMPLATE = ROOT + "content/upload"

    def __init__(self, authorization):
        super(ContentUploadAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def upload(self, data):
        return handle_response(
            requests.post(
                self.TEMPLATE,
                json={"items": data},
                params={"auth": self.authorization.token}))

    def batch_upload(self, data):
        for batch in progress.bar(
            [data[i:i + 1000] for i in range(0, len(data), 1000)]):
            self.upload(batch)
