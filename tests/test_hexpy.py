# -*- coding: utf-8 -*-
"""Tests for hexpy `base.py` module functions."""

import json
import logging
import time

import pytest
from requests.models import Response

from hexpy.base import handle_response, rate_limited


def test_response_error_code():
    """Test status code handled."""
    response = Response()
    response.status_code = 403
    response._content = bytes(json.dumps({"key": "value"}), "utf-8")

    with pytest.raises(ValueError) as e:
        handle_response(response)
    assert e.value.args[0] == 'Something Went Wrong. {"key": "value"}'


def test_response_error_status():
    """Test status json value handled."""
    response = Response()
    response.status_code = 200
    response._content = bytes(json.dumps({"status": "error"}), "utf-8")

    assert response.ok

    with pytest.raises(ValueError) as e:
        handle_response(response)
    assert e.value.args[0] == 'Something Went Wrong. {"status": "error"}'


def test_response_status_ok():
    """Test successful reponse"""
    response = Response()
    response.status_code = 200
    response._content = bytes(json.dumps({"key": "value"}), "utf-8")

    results = handle_response(response)

    assert results == {"key": "value"}


def test_rate_limiting(caplog):
    """Test function rate limiting"""

    def base_func(message: str = "some message"):
        return message

    modified_func = rate_limited(base_func, max_calls=10, period=1)

    with caplog.at_level(logging.INFO):
        for _ in range(12):
            modified_func()

        assert caplog.records[0].msg == "Rate Limit Reached. (Sleeping for 6 seconds)"


def test_rate_limiting_window(caplog):
    """Test sliding window when rate limit not exceeded."""

    def base_func(message: str = "some message"):
        return message

    modified_func = rate_limited(base_func, max_calls=10, period=1)

    with caplog.at_level(logging.INFO):
        for _ in range(12):
            modified_func()
            time.sleep(0.2)
        assert len(caplog.records) == 0
