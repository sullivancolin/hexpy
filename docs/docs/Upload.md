Upload
=========

### Class for working with Content Upload API.

You may use the Content Upload endpoint to upload documents for analysis.
In the past, users have uploaded survey responses, proprietary content,
and other types of data not available in the Crimson Hexagon data library.
To use this endpoint, please contact support and they will create a new custom content type for you. [Reference](https://apidocs.crimsonhexagon.com/reference#content-upload-1)

## Example Usage

```python
>>> from hexpy import CrimsonAuthorization, ContentUploadAPI
>>> auth = CrimsonAuthorization.load_auth_from_file()
>>> upload_client = ContentUploadAPI(auth)
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
upload(data)
```
Upload list of document dictionaries to Crimson Hexagon platform.

If greater than 1000 items passed, reverts to batch upload.
#### Arguments
* data: list of document dictionaries  to upload.

### batch_upload
```python
batch_upload(data)
```
Batch upload list of document dictionaries to Crimson Hexagon platform.

#### Arguments
* data: list of document dictionaries to upload in batches of 1000.
