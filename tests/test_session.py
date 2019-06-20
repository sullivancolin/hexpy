# -*- coding: utf-8 -*-
"""Tests for hexpy `session.py` module."""

import json

import pytest
import responses

from hexpy import HexpySession


@pytest.fixture
def mocked_responses() -> responses.RequestsMock:
    with responses.RequestsMock() as rsps:

        rsps.add(
            responses.GET,
            HexpySession.ROOT
            + "authenticate?username=test&password=testpassword&noExpiration=false&force=false",
            json={"auth": "test-token-00000"},
            status=200,
        )
        yield rsps


def test_login(mocked_responses):
    session = HexpySession.login(username="test", password="testpassword")

    assert session.auth == {"auth": "test-token-00000"}


def test_load_auth(tmp_path):
    HexpySession.TOKEN_FILE = tmp_path / ".hexpy" / "token.json"

    directory = tmp_path / ".hexpy"

    directory.mkdir()

    token_file = directory / "token.json"

    print(token_file, HexpySession.TOKEN_FILE)

    with open(token_file, "w") as outfile:
        json.dump({"auth": "test-token-00000"}, outfile)

    session = HexpySession.load_auth_from_file()

    assert session.auth == {"auth": "test-token-00000"}


def test_save_token(mocked_responses, tmp_path):
    HexpySession.TOKEN_FILE = tmp_path / ".hexpy" / "token.json"
    session = HexpySession.login(username="test", password="testpassword")

    session.save_token()

    with open(tmp_path / ".hexpy" / "token.json") as infile:
        auth = json.load(infile)

    assert auth == {"auth": "test-token-00000"}
