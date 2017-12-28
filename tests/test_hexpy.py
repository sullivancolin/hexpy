# -*- coding: utf-8 -*-
"""Tests for `hexpy` package."""

import pytest
from hexpy.base import response_handler
from hexpy import HexpySession, MonitorAPI
from requests.models import Response
import json


def test_auth():
    pass


def test_response_handler():
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
