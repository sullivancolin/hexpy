# -*- coding: utf-8 -*-
"""Tests for hexpy `session.py` module."""

import json
from pathlib import Path

import pytest
import responses

from hexpy import HexpySession


@pytest.fixture
def mocked_authenticate() -> responses.RequestsMock:
    """Return mocked HexpySession"""
    with responses.RequestsMock() as rsps:

        rsps.add(
            responses.GET,
            HexpySession.ROOT
            + "authenticate?username=test&password=testpassword&noExpiration=false&force=false",
            json={"auth": "test-token-00000"},
            status=200,
        )
        yield rsps


def test_login(mocked_authenticate: responses.RequestsMock) -> None:
    """Test requesting authentication token"""
    session = HexpySession.login(username="test", password="testpassword")

    assert session.auth == {"auth": "test-token-00000"}


def test_load_auth(tmp_path: Path) -> None:
    """Test loading token from file"""
    HexpySession.TOKEN_FILE = tmp_path / ".hexpy" / "token.json"

    directory = tmp_path / ".hexpy"

    directory.mkdir()

    token_file = directory / "token.json"

    with open(token_file, "w") as outfile:
        json.dump({"auth": "test-token-00000"}, outfile)

    session = HexpySession.load_auth_from_file()
    session2 = HexpySession.load_auth_from_file(str(token_file))

    assert session.auth == {"auth": "test-token-00000"}
    assert session2.auth == session.auth


def test_save_token(
    mocked_authenticate: responses.RequestsMock, tmp_path: Path
) -> None:
    """Test saving token to file"""
    HexpySession.TOKEN_FILE = tmp_path / ".hexpy" / "token.json"
    session = HexpySession.login(username="test", password="testpassword")

    session.save_token()

    with open(tmp_path / ".hexpy" / "token.json") as infile:
        auth = json.load(infile)

    assert auth == {"auth": "test-token-00000"}
