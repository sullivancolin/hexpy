# -*- coding: utf-8 -*-
"""Module for uploading custom content"""

from clint.textui import progress
from .base import ROOT, response_handler


class ContentUploadAPI(object):
    """Class for working with Content Upload API.

    You may use the Content Upload endpoint to upload documents for analysis.
    In the past, users have uploaded survey responses, proprietary content,
    and other types of data not available in the Crimson Hexagon data library.
    To use this endpoint, please contact support and they will create a new custom content type for you.

    [Reference](https://apidocs.crimsonhexagon.com/reference#content-upload-1)

    # Example Usage

    ```python
    >>> from hexpy import HexpySession, ContentUploadAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> upload_client = ContentUploadAPI(session)
    >>> items = [
        {
          "title": "Example Title",
          "date": "2010-01-26T16:14:00",
          "author": "me",
          "url": "http://www.crimsonhexagon.com/post1",
          "contents": "Example content",
          "language": "en",
          "type": "Your_Assigned_Content_Type_Name",
          "geolocation": {
            "id": "USA.NY"
          }
        },
      ]
    >>> upload_client.upload(items)
    >>> session.close()
    ```
    """

    TEMPLATE = ROOT + "content/upload"

    def __init__(self, session):
        super(ContentUploadAPI, self).__init__()
        self.session = session.session

    @response_handler
    def upload(self, data):
        """Upload list of document dictionaries to Crimson Hexagon platform.

        If greater than 1000 items passed, reverts to batch upload.
        # Arguments
            data: list of document dictionaries  to upload.
        """
        if len(data) <= 1000:
            return self.session.post(self.TEMPLATE, json={"items": data})
        else:
            print("More than 1000 items found.  Uploading in batches of 1000.")
            return self.batch_upload(data)

    def batch_upload(self, data):
        """Batch upload list of document dictionaries to Crimson Hexagon platform.

        # Arguments
            data: list of document dictionaries to upload in batches of 1000.
        """
        for batch in progress.bar(
            [data[i:i + 1000] for i in range(0, len(data), 1000)]):
            response = self.upload(batch)
        return response