# -*- coding: utf-8 -*-
"""Tests for model validation."""
import logging
from typing import List

import pandas as pd
import pytest
import responses
from _pytest.capture import CaptureFixture
from pandas.io.json import json_normalize
from pydantic import ValidationError

from hexpy import ContentUploadAPI, HexpySession, MonitorAPI, Project
from hexpy.base import JSONDict
from hexpy.models import TrainCollection, TrainItem, UploadCollection, UploadItem


def test_correct_upload_item(upload_items: List[JSONDict]) -> None:
    """Test valid item dictionary is accepted."""
    validated = UploadItem(**upload_items[0])
    assert validated.dict() == upload_items[0]


def test_upload_from_df(upload_items: List[JSONDict]) -> None:
    """Test dataframe for upload can be validated"""
    df = json_normalize(upload_items)
    validated = UploadCollection.from_dataframe(df)
    assert validated == UploadCollection(items=upload_items)


def test_upload_to_df(upload_items: List[JSONDict]) -> None:
    """Test back and forth to dataframe is equal"""
    df = json_normalize(upload_items)
    validated = UploadCollection.from_dataframe(df)
    assert df.equals(validated.to_dataframe()[df.columns])


def test_upload_iteration(upload_items: List[JSONDict]) -> None:
    """Test iteration over collection"""
    validated = UploadCollection(items=upload_items)
    for i, item in zip(range(len(validated)), validated):
        assert validated[i] == item


def test_wrong_upload_item(upload_items: List[JSONDict]) -> None:
    """Test invalid data and error messages"""
    altered = upload_items[0]
    altered["language"] = "engl"
    altered["date"] = "02-2031-01"
    altered["url"] = "incorrect.com"

    with pytest.raises(ValidationError) as e:
        invalid = UploadItem(**altered)  # noqa: F841
    assert e.value.errors() == [
        {
            "loc": ("url",),
            "msg": "url string does not match regex",
            "type": "value_error.url.regex",
        },
        {
            "loc": ("date",),
            "msg": "Could not validate format '02-2031-01'. Must be YYYY-MM-DD or iso-formatted time stamp",
            "type": "value_error",
        },
        {
            "loc": ("language",),
            "msg": "ensure this value has at most 2 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {"limit_value": 2},
        },
    ]


def test_too_many_custom_fields(upload_items: List[JSONDict]) -> None:
    """Test upload has too many custom fields"""

    altered = upload_items[0]
    altered["custom"] = {str(x): str(x) for x in range(15)}

    with pytest.raises(ValidationError) as e:
        invalid = UploadItem(**altered)  # noqa: F841

    assert e.value.errors() == [
        {
            "loc": ("custom",),
            "msg": "15 custom fields found. Must not exceed 10.",
            "type": "value_error",
        }
    ]


def test_long_custom_fields(upload_items: List[JSONDict]) -> None:
    """Test custom field values are too long"""
    altered = upload_items[0]
    altered["custom"] = {"1": "a" * 10_002}

    with pytest.raises(ValidationError) as e:
        invalid = UploadItem(**altered)  # noqa: F841
    assert e.value.errors() == [
        {
            "loc": ("custom",),
            "msg": "Could not validate custom field keys or values. keys must be less that 100 characters. values must be less that 10,000 characters",
            "type": "value_error",
        }
    ]


def test_detect_duplicate_upload_items(upload_items: List[JSONDict]) -> None:
    """Test duplicate items detected"""
    altered = upload_items[1]

    altered["guid"] = "http://www.crimsonhexagon.com/post1"

    with pytest.raises(ValidationError) as e:
        invalid_collection = UploadCollection(items=upload_items)  # noqa: F841

    assert e.value.errors() == [
        {
            "loc": ("items",),
            "msg": "Duplicate item guids detected: ['http://www.crimsonhexagon.com/post1']",
            "type": "value_error",
        }
    ]


def test_unique_upload_items(upload_items: List[JSONDict]) -> None:
    """Test validated dict() is same as original"""
    validated = UploadCollection(items=upload_items)
    assert validated.dict() == upload_items


def test_correct_train_item(train_items: List[JSONDict]) -> None:
    """Test valid train item"""
    validated = TrainItem(**train_items[0])
    assert validated.dict() == train_items[0]


def test_wrong_train_item(train_items: List[JSONDict]) -> None:
    """Test invalid train item and messages"""
    altered = train_items[0]
    altered["language"] = "engl"
    altered["date"] = "02-2031-01"
    altered["url"] = "incorrect.com"
    altered["categoryid"] = None

    with pytest.raises(ValidationError) as e:
        invalid = TrainItem(**altered)  # noqa: F841

    assert e.value.errors() == [
        {
            "loc": ("categoryid",),
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        },
        {
            "loc": ("url",),
            "msg": "url string does not match regex",
            "type": "value_error.url.regex",
        },
        {
            "loc": ("date",),
            "msg": "Could not validate date format '02-2031-01'. Must be YYYY-MM-DD or iso-formatted time stamp",
            "type": "value_error",
        },
        {
            "loc": ("language",),
            "msg": "ensure this value has at most 2 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {"limit_value": 2},
        },
    ]


def test_detect_duplicate_train_items(train_items: List[JSONDict]) -> None:
    """Test duplicate items detected"""
    altered = train_items[1]
    altered["url"] = "http://www.crimsonhexagon.com/post1"

    with pytest.raises(ValidationError) as e:
        invalid_collection = TrainCollection(items=train_items)  # noqa: F841

    assert e.value.errors() == [
        {
            "loc": ("items",),
            "msg": "Duplicate item urls detected: ['http://www.crimsonhexagon.com/post1']",
            "type": "value_error",
        }
    ]


def test_mulitple_category_id(train_items: List[JSONDict]) -> None:
    """Test collection has single category id"""
    altered = train_items[1]
    altered["categoryid"] = 9_107_252_648

    with pytest.raises(ValidationError) as e:
        invalid_collection = TrainCollection(items=train_items)  # noqa: F841

    assert e.value.errors() == [
        {
            "loc": ("items",),
            "msg": "Mulitple `categoryid` values detected: {9107252648, 9107252649}",
            "type": "value_error",
        }
    ]


def test_train_from_df(train_items: List[JSONDict]) -> None:
    """Test from dataframe is same as from dictionary"""
    df = pd.DataFrame.from_records(train_items)
    validated = TrainCollection.from_dataframe(df)
    assert validated == TrainCollection(items=train_items)


def test_train_to_df(train_items: List[JSONDict]) -> None:
    """Test back and forth to dataframe is equal"""
    df = pd.DataFrame.from_records(train_items)
    validated = TrainCollection(items=train_items)
    assert df.equals(validated.to_dataframe()[df.columns])


def test_train_iteration(train_items: List[JSONDict]) -> None:
    """Test iteration over collection"""
    validated = TrainCollection(items=train_items)
    for i, item in zip(range(len(validated)), validated):
        assert validated[i] == item


def test_train_slice(train_items: List[JSONDict]) -> None:
    """Test slicing in collection"""
    validated = TrainCollection(items=train_items)

    assert validated[0:2] == validated


def test_unique_train_items(train_items: List[JSONDict]) -> None:
    """Test items are unique"""
    validated = TrainCollection(items=train_items)
    assert validated.dict() == train_items


@responses.activate
def test_batch_upload(
    upload_items: List[JSONDict], mocked_session: HexpySession, caplog: CaptureFixture
) -> None:
    """Test more than 1000 items are uploaded in batches"""
    responses.add(
        responses.POST, HexpySession.ROOT + "content/upload", json={}, status=200
    )

    items = []

    item = upload_items[0]
    for i in range(3050):
        copy = item.copy()
        copy["guid"] = copy["guid"].replace("post1", f"post{i}")
        items.append(copy)

    collection = UploadCollection(items=items)

    client = ContentUploadAPI(mocked_session)

    with caplog.at_level(logging.INFO):
        response = client.upload(
            document_type=123456789, items=collection, request_usage=True
        )

        assert (
            caplog.records[0].msg
            == "More than 1000 items found.  Uploading in batches of 1000."
        )

    assert response == {"Batch 0": {}, "Batch 1": {}, "Batch 2": {}, "Batch 3": {}}


@responses.activate
def test_batch_train(
    train_items: List[JSONDict], mocked_session: HexpySession, caplog: CaptureFixture
) -> None:
    """Test more than 1000 items are trained in batches"""
    responses.add(
        responses.POST, HexpySession.ROOT + "monitor/train", json={}, status=200
    )

    items = []

    item = train_items[0]
    for i in range(3000):
        copy = item.copy()
        copy["url"] = copy["url"].replace("post1", f"post{i}")
        items.append(copy)

    collection = TrainCollection(items=items)

    client = MonitorAPI(mocked_session)

    with caplog.at_level(logging.INFO):
        response = client.train_monitor(monitor_id=123456789, items=collection)

        assert (
            caplog.records[0].msg
            == "More than 1000 training items found.  Uploading in batches of 1000."
        )

    assert response == {"Batch 0": {}, "Batch 1": {}, "Batch 2": {}}


@responses.activate
def test_project(mocked_session: HexpySession, monitor_details_json: JSONDict) -> None:
    """Test monitor """
    responses.add(
        responses.GET,
        HexpySession.ROOT + "monitor/detail",
        json=monitor_details_json,
        status=200,
    )
    project = Project.get_from_monitor_id(mocked_session, 123456789)

    assert len(project) == 379
    assert len([day for day in project]) == 379
    assert len([day for day in project[:10]]) == 10
