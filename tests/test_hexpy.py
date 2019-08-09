# -*- coding: utf-8 -*-
"""Tests for hexpy `base.py` module functions."""
import logging
import time

import pytest
import requests
import responses
from _pytest.capture import CaptureFixture

from hexpy.base import JSONDict, handle_response, rate_limited


@responses.activate
def test_response_error_code() -> None:
    """Test status code handled."""

    responses.add(
        responses.GET,
        "https://testsite.com/endpoint",
        json={"key": "value"},
        status=403,
    )

    response = requests.get("https://testsite.com/endpoint")

    with pytest.raises(ValueError) as e:
        handle_response(response)
    assert e.value.args[0] == 'Something Went Wrong. {"key": "value"}'


@responses.activate
def test_response_error_status() -> None:
    """Test status json value handled."""
    responses.add(
        responses.GET,
        "https://testsite.com/endpoint",
        json={"status": "error"},
        status=200,
    )

    response = requests.get("https://testsite.com/endpoint")
    assert response.ok

    with pytest.raises(ValueError) as e:
        handle_response(response)
    assert e.value.args[0] == 'Something Went Wrong. {"status": "error"}'


@responses.activate
def test_response_status_ok() -> None:
    """Test successful reponse"""
    responses.add(
        responses.GET,
        "https://testsite.com/endpoint",
        json={"key": "value"},
        status=200,
    )

    response = requests.get("https://testsite.com/endpoint")
    results = handle_response(response)

    assert results == {"key": "value"}


def test_rate_limiting(caplog: CaptureFixture) -> None:
    """Test function rate limiting"""

    def base_func(message: str = "some message") -> JSONDict:
        return {"msg": message}

    modified_func = rate_limited(base_func, max_calls=10, period=1)

    with caplog.at_level(logging.INFO):
        for _ in range(12):
            modified_func()

        assert caplog.records[0].msg == "Rate Limit Reached. (Sleeping for 6 seconds)"


def test_rate_limiting_window(caplog: CaptureFixture) -> None:
    """Test sliding window when rate limit not exceeded."""

    def base_func(message: str = "some message") -> JSONDict:
        return {"msg": message}

    modified_func = rate_limited(base_func, max_calls=10, period=1)

    with caplog.at_level(logging.INFO):
        for _ in range(12):
            modified_func()
            time.sleep(0.2)
        assert len(caplog.records) == 0
