# -*- coding: utf-8 -*-
"""Tests for model validation."""
import logging
from typing import List

import pandas as pd
import pytest
import responses
from pandas.io.json import json_normalize
from pydantic import ValidationError

from hexpy import ContentUploadAPI, HexpySession, MonitorAPI
from hexpy.base import JSONDict
from hexpy.models import TrainCollection, TrainItem, UploadCollection, UploadItem


def test_correct_upload_item(upload_items: List[JSONDict]):
    """Test valid item dictionary is accepted."""
    validated = UploadItem(**upload_items[0])
    assert validated.dict() == upload_items[0]


def test_upload_from_df(upload_items: List[JSONDict]):
    """Test dataframe fore upload can be validated"""
    df = json_normalize(upload_items)
    validated = UploadCollection.from_dataframe(df)
    assert validated == UploadCollection(items=upload_items)


def test_upload_to_df(upload_items: List[JSONDict]):
    df = json_normalize(upload_items)
    validated = UploadCollection.from_dataframe(df)
    assert df.equals(validated.to_dataframe())


def test_upload_iteration(upload_items: List[JSONDict]):
    validated = UploadCollection(items=upload_items)
    for i, item in zip(range(len(validated)), validated):
        assert validated[i] == item


def test_wrong_upload_item(upload_items: List[JSONDict]):

    altered = upload_items[0]
    altered["language"] = "engl"
    altered["date"] = "02-2031-01"
    altered["url"] = "incorrect.com"

    with pytest.raises(ValidationError) as e:
        invalid = UploadItem(**altered)

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


def test_detect_duplicate_upload_items(upload_items: List[JSONDict]):
    altered = upload_items[1]

    altered["guid"] = "http://www.crimsonhexagon.com/post1"

    with pytest.raises(ValidationError) as e:
        invalid_collection = UploadCollection(items=upload_items)

    assert e.value.errors() == [
        {
            "loc": ("items",),
            "msg": "Duplicate item guids detected: ['http://www.crimsonhexagon.com/post1']",
            "type": "value_error",
        }
    ]


def test_unique_upload_items(upload_items: List[JSONDict]):
    validated = UploadCollection(items=upload_items)
    assert validated.dict() == upload_items


def test_correct_train_item(train_items: List[JSONDict]):
    validated = TrainItem(**train_items[0])
    assert validated.dict() == train_items[0]


def test_wrong_train_item(train_items: List[JSONDict]):

    altered = train_items[0]
    altered["language"] = "engl"
    altered["date"] = "02-2031-01"
    altered["url"] = "incorrect.com"
    altered["categoryid"] = None

    with pytest.raises(ValidationError) as e:
        invalid = TrainItem(**altered)

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


def test_detect_duplicate_train_items(train_items: List[JSONDict]):
    altered = train_items[1]
    altered["url"] = "http://www.crimsonhexagon.com/post1"

    with pytest.raises(ValidationError) as e:
        invalid_collection = TrainCollection(items=train_items)

    assert e.value.errors() == [
        {
            "loc": ("items",),
            "msg": "Duplicate item urls detected: ['http://www.crimsonhexagon.com/post1']",
            "type": "value_error",
        }
    ]


def test_mulitple_category_id(train_items: List[JSONDict]):
    altered = train_items[1]
    altered["categoryid"] = 9_107_252_648

    with pytest.raises(ValidationError) as e:
        invalid_collection = TrainCollection(items=train_items)

    assert e.value.errors() == [
        {
            "loc": ("items",),
            "msg": "Mulitple `categoryid` values detected: {9107252648, 9107252649}",
            "type": "value_error",
        }
    ]


def test_train_from_df(train_items: List[JSONDict]):
    df = pd.DataFrame.from_records(train_items)
    validated = TrainCollection.from_dataframe(df)
    assert validated == TrainCollection(items=train_items)


def test_train_to_df(train_items: List[JSONDict]):
    df = pd.DataFrame.from_records(train_items)
    validated = TrainCollection.from_dataframe(df)
    assert df.equals(validated.to_dataframe())


def test_train_iteration(train_items: List[JSONDict]):
    validated = TrainCollection(items=train_items)
    for i, item in zip(range(len(validated)), validated):
        assert validated[i] == item


def test_train_slice(train_items: List[JSONDict]):
    validated = TrainCollection(items=train_items)

    assert validated[0:2] == validated


def test_unique_train_items(train_items: List[JSONDict]):
    validated = TrainCollection(items=train_items)
    assert validated.dict() == train_items


@responses.activate
def test_batch_upload(upload_items, mocked_session, caplog):
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
def test_batch_train(train_items, mocked_session, caplog):
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
