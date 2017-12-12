# -*- coding: utf-8 -*-
"""Tests for `hexpy` package."""

import pytest
from hexpy.base import response_handler
from hexpy import Timestamp, CrimsonAuthorization, MonitorAPI


def test_auth():
    pass


def test_handle_response():
    from requests.models import Response
    import json
    r1 = Response()
    r1.status_code = 403
    r1._content = bytes(json.dumps({"status": "error"}), 'utf-8')

    @response_handler
    def test_response(r):
        return r

    with pytest.raises(ValueError) as e:
        test_response(r1)
    r1.status_code = 200
    with pytest.raises(ValueError) as e:
        test_response(r1)

    data = {"some": "suff"}
    r1._content = bytes(json.dumps({"some": "stuff"}), 'utf-8')


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
