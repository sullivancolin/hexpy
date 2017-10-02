# -*- coding: utf-8 -*-
"""Module for uploading custom content"""

import requests
from ratelimiter import RateLimiter
from clint.textui import progress
from .response import handle_response
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class ContentUploadAPI(object):
    """Class for working with Content Upload API.

    You may use the Content Upload endpoint to upload documents for analysis.
    In the past, users have uploaded survey responses, proprietary content,
    and other types of data not available in the Crimson Hexagon data library.
    To use this endpoint, please contact support and they will create a new custom content type for you.

    [Reference](https://apidocs.crimsonhexagon.com/reference#content-upload-1)
    """

    TEMPLATE = ROOT + "content/upload"

    def __init__(self, authorization):
        super(ContentUploadAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def upload(self, data):
        """Upload list of document dictionaries to Crimson Hexagon platform.

        If greater than 1000 items passed, reverts to batch upload.
        # Arguments
            data: list of document dictionaries  to upload.

        """
        if len(data) <= 1000:

            return handle_response(
                requests.post(
                    self.TEMPLATE,
                    json={"items": data},
                    params={"auth": self.authorization.token}))
        else:
            print("More than 1000 items found.  Uploading in batches of 1000.")
            self.batch_upload(data)

    def batch_upload(self, data):
        """Batch upload list of document dictionaries to Crimson Hexagon platform.

        # Arguments
            data: list of document dictionaries to upload in batches of 1000.

        """
        for batch in progress.bar(
            [data[i:i + 1000] for i in range(0, len(data), 1000)]):
            self.upload(batch)
