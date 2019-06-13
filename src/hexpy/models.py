from collections import Counter
from typing import Dict, List, Optional

import ftfy
import pandas as pd
import pendulum
from pendulum.exceptions import ParserError
from pydantic import BaseModel, Schema, UrlStr, validator


class UploadItem(BaseModel):
    """Validation model for an item of content to be uploaded.

    Checks for required fields, with valid types and formatting.

    ## Fields
        * type: str
        * title: str
        * url: UrlStr
        * author: str
        * language: str(max_length=2, min_length=2)
        * date: str
        * contents: str
        * geolocation: Optional[Dict[str, str]] = None

    ## Example Usage

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
    """

    type: str
    title: str
    url: UrlStr
    author: str
    language: str = Schema(..., max_length=2, min_length=2)  # type: ignore
    date: str
    contents: str
    geolocation: Optional[Dict[str, str]] = None

    class Config:
        allow_mutation = False

    @validator("date")
    def parse_datetime(cls, value) -> str:
        """Validate date string using pendulum parsing followed by ISO formatting."""
        try:
            date = pendulum.parse(value)
        except ParserError:
            try:
                date = pendulum.from_format(value, "MM/DD/YY HH:mm")
            except Exception:
                raise ValueError(
                    f"Could not validate format '{value}'. Must be YYYY-MM-DD or iso-formatted time stamp"
                )
        return date.to_iso8601_string()

    @validator("contents")
    def fix_contents(cls, value) -> str:
        """Fix mojibake in contents"""
        return ftfy.fix_text(value)

    @validator("title")
    def fix_title(cls, value) -> str:
        """Fix mojibake in title"""
        return ftfy.fix_text(value)

    @validator("author")
    def fix_author(cls, value) -> str:
        """Fix mojibake in author"""
        return ftfy.fix_text(value)

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.url == other.url

    def __repr__(self):  # pragma: no cover
        return f"<UploadItem url='{self.url}'>"


class UploadCollection(BaseModel):
    """Validation model for collection of items to be uploaded.

    Checks for duplicate upload items. Easily convert to/from dataframe

    ## Fields
        * items: List[UploadItem]

    ## Example Usage

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
    """

    items: List[UploadItem]

    class Config:
        allow_mutation = False

    @validator("items", whole=True)
    def unique_item_urls(cls, items):
        if len(items) != len(set(items)):
            counts = Counter(items)
            dups = [tup for tup in counts.most_common() if tup[1] > 1]
            dups = [tup[0].url for tup in dups]
            raise ValueError(f"Duplicate item urls detected: {dups}")

        return items

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        """Create UploadCollection from pandas DataFrame containing necessary fields

        ## Arguments:
            * df: pd.DataFrame
        """
        records = df.to_dict(orient="records")
        return cls(items=records)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert UploadCollection to pandas Dataframe with one colume for each field"""
        return pd.DataFrame.from_records(self.dict())

    def dict(self, *args, **kwargs):
        return [rec.dict() for rec in self.items]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, slice):
        return self.items[slice]


class TrainItem(BaseModel):
    """Validation model for training post to be uploaded.

    Checks for required fields, with valid types and formatting.

    ## Fields
        * categoryid: int
        * title: str
        * url: UrlStr
        * author: str
        * language: str(max_length=2, min_length=2)
        * date: str
        * contents: str

    ## Example Usage

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
    """

    categoryid: int
    title: str
    url: UrlStr
    author: str
    language: str = Schema(..., max_length=2, min_length=2)  # type: ignore
    date: str
    contents: str

    class Config:
        """Immutable Object"""

        allow_mutation = False

    @validator("date")
    def parse_datetime(cls, value):
        """Validate date string using pendulum parsing followed by ISO formatting."""
        try:
            date = pendulum.parse(value)
        except ParserError:
            try:
                date = pendulum.from_format(value, "MM/DD/YY HH:mm")
            except Exception:
                raise ValueError(
                    f"Could not validate date format '{value}'. Must be YYYY-MM-DD or iso-formatted time stamp"
                )
        return date.to_iso8601_string()

    @validator("contents")
    def fix_contents(cls, value) -> str:
        """Fix mojibake in contents"""
        return ftfy.fix_text(value)

    @validator("title")
    def fix_title(cls, value) -> str:
        """Fix mojibake in title"""
        return ftfy.fix_text(value)

    @validator("author")
    def fix_author(cls, value) -> str:
        """Fix mojibake in author"""
        return ftfy.fix_text(value)

    def __hash__(self):
        """Identify unique object by url"""
        return hash(self.url)

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.url == other.url

    def __repr__(self):  # pragma: no cover
        return f"<TrainItem url='{self.url}'>"


class TrainCollection(BaseModel):
    """Validation model for collections of training posts to be uploaded.

    Checks for duplicate training posts. Easily convert to/from dataframe

    ## Fields
        * items: List[TrainItem]

    ## Example Usage

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
    >>> train_collection = TrainCollection(items=items)
    ```
    """

    items: List[TrainItem]

    class Config:
        """Immutable Object"""

        allow_mutation = False

    @validator("items", whole=True)
    def unique_item_urls(cls, items):
        if len(items) != len(set(items)):
            counts = Counter(items)
            dups = [tup for tup in counts.most_common() if tup[1] > 1]
            dups = [tup[0].url for tup in dups]
            raise ValueError(f"Duplicate item urls detected: {dups}")

        return items

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        """Create TrainCollection from pandas DataFrame containing necessary fields

        ## Arguments:
            * df: pd.DataFrame
        """
        records = df.to_dict(orient="records")
        return cls(items=records)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert TrainCollection to pandas Dataframe with one colume for each Field"""
        return pd.DataFrame.from_records(self.dict())

    def dict(self, *args, **kwargs):
        return [rec.dict() for rec in self.items]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for item in self.items:
            yield item

    def __getitem__(self, slice):
        return self.items[slice]
