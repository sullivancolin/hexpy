path: blob/master/hexpy/src
source:  models.py

Data Validation
===============

[Pydantic Style Classes](https://pydantic-docs.helpmanual.io/) for validating data for [Custom Content Upload](Upload.md#upload) and [BrightView Training](Monitor.md#train_monitor)

## `UploadItem`
Validation model for an item of custom content to be uploaded. Checks for required fields, with valid types and formatting.

### Fields
* type: String, Custom Content Type Name
* title: String, Document Title
* url: Url, Unique Document Url
* author: String, Document Author
* language: String, 2 letter langauge code
* date: String, Date or Datetime
* contents: String, Document Body
* geolocation: Optional Mapping Identifier


### Example Usage

```python
>>> from hexpy.models import UploadItem
>>> item_dict = {
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
    }
>>> upload_item = UploadItem(**item_dict)
```

## `UploadCollection`
Validation model for collection of items to be uploaded. Checks for duplicate upload items, easily convert to/from dataframe

### Fields
* items: List of UploadItems or valid dictionaries

### Example Usage

```python
>>> from hexpy.models import UploadItem, UploadCollection
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
        }
    ]
>>> upload_collection = UploadCollection(items=items)
```

### Methods

### from_dataframe
```python
from_dataframe(df: pd.DataFrame) -> UploadCollection
```
Create UploadCollection from pandas DataFrame containing necessary fields.

#### Arguments:
* df: pd.DataFrame

### to_dataframe
 ```python
 to_dataframe() -> pd.DataFrame
 ```
 Convert UploadCollection to pandas Dataframe with one colume for each field.

## `TrainItem`
Validation model for training post to be uploaded. Checks for required fields, with valid types and formatting.

### Fields
* type: String, Custom Content Type Name
* title: String, Document Title
* url: Url, Unique Document Url
* author: String, Document Author
* language: String, 2 letter langauge code
* date: String, Date or Datetime
* contents: String, Document Body
* categoryid: Integer of Category defined in Monitor

### Example Usage

```python
>>> from hexpy.models import TrainItem
>>> item_dict = {
    "title": "Example Title",
    "date": "2010-01-26T16:14:00",
    "author": "me",
    "url": "http://www.crimsonhexagon.com/post1",
    "contents": "Example content",
    "language": "en",
    "categoryid": 9107252649,
}
>>> train_item = TrainItem(**item)
```

## `TrainCollection`
Validation model for collections of training posts to be uploaded. Checks for duplicate training posts, easily convert to/from dataframe


### Fields
* items: List of TrainItems or valid dictionaries

### Example Usage

```python
>>> from hexpy.models import TrainItem, TrainCollection
>>> items = [
    {
        "title": "Example Title",
        "date": "2010-01-26T16:14:00",
        "author": "me",
        "url": "http://www.crimsonhexagon.com/post1",
        "contents": "Example content",
        "language": "en",
        "categoryid": 9107252649,
    }
]
>>> train_collection = TrainCollection(items=items])
```
### Methods

### from_dataframe
```python
from_dataframe(df: pd.DataFrame) -> TrainCollection
```
Create TrainCollection from pandas DataFrame containing necessary fields.

#### Arguments:
* df: pd.DataFrame

### to_dataframe
 ```python
 to_dataframe() -> pd.DataFrame
 ```
 Convert TrainCollection to pandas Dataframe with one colume for each field.
