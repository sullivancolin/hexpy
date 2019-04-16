path: blob/master/hexpy
source: content_upload.py

Upload API
=========

### Class for working with Content Upload API.

You may use the Content Upload endpoint to upload documents for analysis.
In the past, users have uploaded survey responses, proprietary content,
and other types of data not available in the Crimson Hexagon data library.
To use this endpoint, please contact support and they will create a new custom content type for you. [Reference](https://apidocs.crimsonhexagon.com/reference#content-upload-1)

## Example Usage

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
```
## Methods

### upload
```python
upload(data: Sequence[Dict[str, Any]]) -> Dict[str, Any]
```
Upload list of document dictionaries to Crimson Hexagon platform.

If greater than 1000 items passed, reverts to batch upload.
#### Arguments
* data: list of document dictionaries  to upload.

### batch_upload
```python
batch_upload(data: Sequence[Dict[str, Any]]) -> Dict[str, Any]
```
Batch upload list of document dictionaries to Crimson Hexagon platform.

#### Arguments
* data: list of document dictionaries to upload in batches of 1000.

### custom_field_upload
```python
custom_field_upload(document_type: int, batch: int, data: Sequence[Dict[str, Any]]) -> Dict[str, Any]
```
Upload content via the API w/ custom fields support.

#### Arguments
* document_type: Integer, The id of the document type to which the uploading docs will belong
* batch: Integer, The id of the batch to which the uploading docs will belong.
* data: list of document dictionaries  to upload.

### delete_content
```python
delete_content(document_type: int) -> Dict[str, Any]
```
Content deletion via the API.

#### Arguments
* documentType: Integer, The id of the document type to delete.
* removeResults: Boolean, If true, removes the results associated with the documentType.

### delete_content_batch
```python
delete_content_batch(document_type: int, batch: int) -> Dict[str, Any]
```
Delete batch content via the API.

#### Arguments
* documentType: Integer, The id of the document type to delete documents from.
* batch: String, The id of the document batch to delete.

### create_content_source
```python
create_content_source(content_source) -> Dict[str, Any]
```
Content Source creation.

### delete_content_source
```python
delete_content_type(document_type: int, remove_results: bool) -> Dict[str, Any]
```
Content Source deletion.

### list_content_sources
```python
list_content_sources(team_id: int) -> Dict[str, Any]
```
Content Source list.

#### Arguments
* team: Integer, The id of the team to which the listed content sources belong.