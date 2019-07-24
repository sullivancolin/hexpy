"""Module for uploading custom content"""

import inspect
import logging

from .base import JSONDict, handle_response, rate_limited
from .models import UploadCollection
from .session import HexpySession

logger = logging.getLogger(__name__)


class ContentUploadAPI:
    """Class for working with Content Upload API.

    The Custom Content Upload endpoint enables the uploading of documents for analysis in the Forsight Platform.
    Users have uploaded survey responses, proprietary content, and other types of data not available in the Crimson Hexagon data library.
    To use this endpoint, please contact support and they will create a new custom content type for you.

    [Reference](https://apidocs.crimsonhexagon.com/reference#content-upload)

    # Example Usage

    ```python
    >>> from hexpy import HexpySession, ContentUploadAPI
    >>> from hexpy.models import UploadCollection, UploadItem
    >>> session = HexpySession.load_auth_from_file()
    >>> upload_client = ContentUploadAPI(session)
    >>> items = [
    {
        "date": "2010-01-26T16:14:00",
        "contents": "Example content",
        "guid": "This is my guid",
        "title": "Example Title",
        "author": "me",
        "language": "en",
        "gender": "F",
        "geolocation": {
            "id": "USA.NY"
        },
        "pageId": "This is a pageId",
        "parentGuid": "123123",
        "authorProfileId": "1234567",
        "custom": {
            "field0": "value0",
            "field1": "45.2",
            "field2": "123",
            "field3": "value3",
            "field4": "value4",
            "field5": "5_stars",
            "field6": "1200",
            "field7": "5",
            "field8": "value5",
            "field9": "value6"
        }
    }
]
    >>> data = UploadCollection(items=items)
    >>> upload_client.upload(data)
    ```
    """

    def __init__(self, session: HexpySession) -> None:
        self.session = session.session
        self.TEMPLATE = session.ROOT + "content/"
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in ["batch_upload", "__init__"]:
                setattr(
                    self, name, rate_limited(fn, session.MAX_CALLS, session.ONE_MINUTE)
                )

    def upload(
        self, document_type: int, items: UploadCollection, request_usage=True
    ) -> JSONDict:
        """Upload collection of Custom Content to Crimson Hexagon platform.

        If greater than 1000 items passed, reverts to batch upload.
        # Arguments
            document_type: Integer, The id of the document type to which the uploading docs will belong.
            items: validated UploadCollection.
            requestUsage: Bool, return usage information.
        """
        if len(items) > 1000:
            logger.info("More than 1000 items found.  Uploading in batches of 1000.")
            return self.batch_upload(
                document_type=document_type, items=items, request_usage=request_usage
            )

        return handle_response(
            self.session.post(
                self.TEMPLATE + "upload",
                params={"documentType": document_type},
                json={"items": items.dict(skip_defaults=True)},
            )
        )

    def batch_upload(
        self, document_type: int, items: UploadCollection, request_usage=True
    ) -> JSONDict:
        """Batch upload collection of Custom Content to Crimson Hexagon platform in groups of 1000.

        # Arguments
            document_type: Integer, The id of the document type to which the uploading docs will belong.
            items: validated UploadCollection.
            requestUsage: Bool, return usage information.

        """
        batch_responses = {}
        for batch_num, batch in enumerate(
            [items[i : i + 1000] for i in range(0, len(items), 1000)]
        ):
            response = self.upload(document_type, batch, request_usage)
            logger.info(f"Uploaded batch number: {batch_num}")
            batch_responses[f"Batch {batch_num}"] = response
        return batch_responses

    def delete_content_batch(self, document_type: int, batch: str) -> JSONDict:
        """Delete single batch of custom content via the API.

        # Arguments
            * documentType: Integer, The id of the document type to delete documents from.
            * batch: String, The id of the document batch to delete.
        """
        return handle_response(
            self.session.post(
                self.TEMPLATE + "delete",
                params={"documentType": document_type, "batch": batch},
            )
        )

    def delete_content_items(
        self, document_type: int, items: JSONDict, batch: str = None
    ) -> JSONDict:
        """Delete individual custom content documents via guid or url.

        # Arguments
            * documentType: Integer, The id of the document type to delete documents from.
            * items: JSONDict, dictionary specifying which documents to delete.
            * batch: String, Batch ID.

        Example Items:
        ```python
        {
            "items": [
                {
                    "guid": "This is my guid",
                    "url": "http://www.crimsonhexagon.com/post1"
                }
            ]
        }
        ```
        """
        return handle_response(
            self.session.post(
                self.TEMPLATE + "delete",
                params={"documentType": document_type, "batch": batch, "url": url},
                json=items,
            )
        )

    def delete_content_source(
        self, document_type: int, remove_results: bool
    ) -> JSONDict:
        """Content Source deletion.

        # Arguments
            * documentType: Integer, The id of the document type to delete/
            * removeResults: Boolean, If true, removes the results associated with the documentType.
        """
        return handle_response(
            self.session.delete(
                self.TEMPLATE + "sources",
                params={"documentType": document_type, "removeResults": remove_results},
            )
        )

    def create_content_source(self, content_type: JSONDict) -> JSONDict:
        """Content Source creation.

        Example content_type:
        ```python
        {
            "teamid": 461777351,
            "name": "Customer_Surveys",
            "description": "Customer Survey, May 2019"
        }
        ```
        """
        return handle_response(
            self.session.post(self.TEMPLATE + "sources", json=content_type)
        )

    def list_content_sources(self, team_id: int) -> JSONDict:
        """
        Content Source list.

        # Arguments
            * team: Integer, The id of the team to which the listed content sources belong.
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "sources/list", params={"team": team_id})
        )
