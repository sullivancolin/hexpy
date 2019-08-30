# -*- coding: utf-8 -*-
"""Test Fixtures."""

import json
from typing import List

import pandas as pd
import pytest
from pandas.io.json import json_normalize

from hexpy import HexpySession
from hexpy.base import JSONDict


@pytest.fixture
def upload_items() -> List[JSONDict]:
    """Raw list of upload dictionaries"""
    return [
        {
            "title": "Example Title",
            "date": "2010-01-26T16:14:00+00:00",
            "guid": "http://www.crimsonhexagon.com/post1",
            "author": "me",
            "url": "http://www.crimsonhexagon.com/post1",
            "contents": "Example content",
            "language": "en",
            "gender": "M",
        },
        {
            "title": "Example Title",
            "date": "2010-01-26T16:14:00+00:00",
            "author": "me",
            "url": "http://www.crimsonhexagon.com/post2",
            "guid": "http://www.crimsonhexagon.com/post2",
            "contents": "Example content",
            "language": "en",
            "geolocation": {"id": "USA.NY"},
        },
        {
            "date": "2010-01-26T16:14:00+00:00",
            "contents": "Example content",
            "url": "http://www.crimsonhexagon.com/post3",
            "guid": "http://www.crimsonhexagon.com/post3",
            "title": "Example Title",
            "author": "me",
            "language": "en",
            "custom": {"CF1": "CF1_value", "CF2": "CF2_45.2", "CF3": "CF3_123"},
            "gender": "F",
            "pageId": "This is a pageId",
            "parentGuid": "123123",
            "authorProfileId": "1234567",
            "engagementType": "REPLY",
        },
    ]


@pytest.fixture
def upload_dataframe(upload_items: List[JSONDict]) -> pd.DataFrame:
    """Pandas dataframe of upload content"""
    return json_normalize(upload_items)


@pytest.fixture
def duplicate_items(upload_items: List[JSONDict]) -> List[JSONDict]:
    """Upload items with duplicates"""
    upload_items[1]["guid"] = upload_items[0]["guid"]

    return upload_items


@pytest.fixture
def train_items() -> List[JSONDict]:
    """Raw list of training dictionaries"""
    return [
        {
            "title": "Example Title",
            "date": "2010-01-26T16:14:00+00:00",
            "author": "me",
            "url": "http://www.crimsonhexagon.com/post1",
            "contents": "Example content",
            "language": "en",
            "categoryid": 9_107_252_649,
        },
        {
            "title": "Example Title",
            "date": "2010-01-26T16:14:00+00:00",
            "author": "me",
            "url": "http://www.crimsonhexagon.com/post2",
            "contents": "Example content",
            "language": "en",
            "categoryid": 9_107_252_649,
        },
    ]


@pytest.fixture
def train_dataframe(train_items: List[JSONDict]) -> pd.DataFrame:
    """Pandas dataframe of train items"""
    return pd.DataFrame.from_records(train_items)


@pytest.fixture
def fake_session() -> HexpySession:
    """return mocked HexpySession"""
    return HexpySession(token="test-token-00000")


@pytest.fixture
def posts_json() -> JSONDict:
    """Raw sample posts JSON"""
    with open("tests/test_data/test_posts.json") as infile:
        posts = json.load(infile)

    return posts


@pytest.fixture
def posts_df() -> pd.DataFrame:
    """Expected output for converting posts JSON to df"""
    df = pd.read_csv("tests/test_data/test_df.csv")
    return df


@pytest.fixture
def json_documentation() -> JSONDict:
    """Raw api documentation json"""
    with open("tests/test_data/test_docs.json") as infile:
        return json.load(infile)


@pytest.fixture
def markdown_documentation() -> str:
    """Expected output for api documentation formating"""
    with open("tests/test_data/test_docs.md") as infile:
        return infile.read()


@pytest.fixture
def geography_json() -> JSONDict:
    """Expected format of geography metadata"""
    with open("tests/test_data/geography.json") as infile:
        return json.load(infile)


@pytest.fixture
def results_json() -> JSONDict:
    """Expected monitor results json"""
    with open("tests/test_data/results.json") as infile:
        return json.load(infile)


@pytest.fixture
def monitor_details_json() -> JSONDict:
    """Expected monitor details json"""
    with open("tests/test_data/monitor_details.json") as infile:
        return json.load(infile)
