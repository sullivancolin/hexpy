path: blob/master/src/hexpy
source: content_upload.py

Upload API
=========

Class for working with the Custom Content Upload API.

The Custom Content Upload endpoint enables the uploading of documents for analysis in the Forsight Platform.
Users have uploaded survey responses, proprietary content, and other types of data not available in the Crimson Hexagon data library.

## Example Usage
<div class="termy">

```python
>>> from hexpy import HexpySession, ContentUploadAPI
>>> from hexpy.models import UploadCollection
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
</div>

## Methods

### upload
```python
upload(document_type: int, items: UploadCollection, request_usage=True) -> JSONDict
```
Upload collection of documents to Crimson Hexagon platform.

If greater than 1000 items passed, reverts to batch upload.

#### Arguments
* document_type: Integer, The id of the document type to which the uploading docs will * belong.
* items: validated [UploadCollection](Data_Validation.#uploadcollection]).
* requestUsage: Bool, return usage information.

### batch_upload
```python
batch_upload(document_type: int, items: UploadCollection, request_usage=True) -> JSONDict
```
Batch upload collection of Custom Content to Crimson Hexagon platform in groups of 1000.

#### Arguments
    * document_type: Integer, The id of the document type to which the uploading docs will belong.
    * items: validated UploadCollection.
    * requestUsage: Bool, return usage information.

### delete_content_items
```python
delete_content_items(document_type: int, items: List[JSONDict], batch: str = None) -> JSONDict:
```
Delete individual custom content documents via guid or url.

Example content_type:
```python
[
    {
        "guid": "This is my guid",
        "url": "http://www.crimsonhexagon.com/post1"
    }
]
```

#### Arguments
* documentType: Integer, The id of the document type to delete.
* removeResults: Boolean, If true, removes the results associated with the documentType.

### delete_content_batch
```python
delete_content_batch(document_type: int, batch: int) -> JSONDict
```
Delete single batch of custom content via the API.

#### Arguments
* documentType: Integer, The id of the document type to delete documents from.
* batch: String, The id of the document batch to delete.

### create_content_source
```python
create_content_source(content_type: JSONDict) -> JSONDict
```
Content Source creation.

Example content_type
```python
{
    "teamid": 461777351,
    "name": "Customer_Surveys",
    "description": "Customer Survey, May 2019"
}
```

### delete_content_source
```python
delete_content_type(document_type: int, remove_results: bool) -> JSONDict
```
Content Source deletion.

### list_content_sources
```python
list_content_sources(team_id: int) -> JSONDict
```
Content Source list.

#### Arguments
* team: Integer, The id of the team to which the listed content sources belong.