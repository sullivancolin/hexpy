#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `hexpy` package."""
from unittest.mock import Mock, patch
import pytest
from hexpy import handle_response
from hexpy import Timestamp, CrimsonAuthorization
from hexpy import CrimsonAuthorization, MonitorAPI


@patch('hexpy.monitor.requests.get')
def test_rate_limit(mock_get):
    auth = CrimsonAuthorization.load_auth_from_cache()

    client = MonitorAPI(auth)
    mock_get.return_value.status_code = 200
    for i in range(300):
        if i % 10 == 0:
            print(i)
        client.details(6054759047)


def test_auth():
    pass


def test_handle_response():
    from requests.models import Response
    import json
    r1 = Response()
    r1.status_code = 403
    r1._content = bytes(json.dumps({"error": "something went wrong"}), 'utf-8')

    with pytest.raises(ValueError) as e:
        handle_response(r1)

    r1.status_code = 200

    with pytest.raises(ValueError) as e:
        handle_response(r1, check_text=True)

    data = {"error": "something went wrong"}

    assert (handle_response(r1) == data)


def test_timestamp_from_string():

    stamp = Timestamp.from_string("2017-04-29T00:00:00")

    assert (stamp.year == 2017)
    assert (stamp.month == 4)
    assert (stamp.day == 29)
    assert (stamp.hour == 0)
    assert (stamp.minute == 0)
    assert (stamp.second == 0)


def test_timestamp_to_string():

    stamp = Timestamp(2017, 4, 29, 0, 0, 0)
    assert (stamp.to_string() == "2017-04-29T00:00:00")
