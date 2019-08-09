# -*- coding: utf-8 -*-
"""Tests for cli `hexpy` module."""

import json
from pathlib import Path
from typing import List

import pandas as pd
import pytest
import responses
from _pytest.monkeypatch import MonkeyPatch
from click.testing import CliRunner
from pydantic import ValidationError

from hexpy import HexpySession, hexpy
from hexpy.base import JSONDict
from hexpy.hexpy import cli, docs_to_text, helpful_validation_error, posts_json_to_df
from hexpy.models import TrainCollection, UploadCollection


def fake_login(force: bool = False, expiration: bool = True) -> HexpySession:
    """Function to replace real login function"""
    return HexpySession(token="test-token-00000")


def test_cli_help() -> None:
    """Test cli help text"""

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert (
        result.output
        == """Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n  Command Line interface for working with Crimson Hexagon API.\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  api-documentation  Get API documentation for all endpoints.\n  export             Export monitor posts as json or to a spreadsheet.\n  login              Get API token with username and password and save to...\n  metadata           Get Metadata for account team, monitors, and geography.\n  results            Get Monitor results for 1 or more metrics.\n  stream-posts       Stream posts in real time, stop after a maximum of 10K.\n  train              Upload spreadsheet file of training examples for monitor.\n  upload             Upload spreadsheet file as custom content.\n"""
    )


def test_posts_json_to_df(posts_json: List[JSONDict], posts_df: pd.DataFrame) -> None:
    """Test covert posts json to dataframe"""
    df = posts_json_to_df(posts_json, images=True)
    assert df.equals(posts_df[df.columns])


def test_format_documentation(
    json_documentation: JSONDict, markdown_documentation: str
) -> None:
    """Test coverting json api documentation to markdown"""
    docs = docs_to_text(json_documentation, mode="md")
    assert markdown_documentation == docs


@responses.activate
def test_export(posts_json: JSONDict, monkeypatch: MonkeyPatch) -> None:
    """Test exporting posts from cli to json"""

    monkeypatch.setattr(hexpy, "login", fake_login)

    responses.add(
        responses.GET,
        HexpySession.ROOT + "monitor/posts",
        json={"posts": posts_json},
        status=200,
    )
    responses.add(
        responses.GET,
        HexpySession.ROOT + "monitor/detail",
        json={"resultsStart": "day1", "resultsEnd": "day2", "name": "test_monitor"},
        status=200,
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["export", "-o", "json", "123456789"])
    assert result.output.strip() == "\n".join([json.dumps(x) for x in posts_json])


@responses.activate
def test_api_documentation(
    json_documentation: JSONDict, monkeypatch: MonkeyPatch
) -> None:
    """Test cli api-documentation """

    monkeypatch.setattr(hexpy, "login", fake_login)

    responses.add(
        responses.GET,
        HexpySession.ROOT + "documentation",
        json=json_documentation,
        status=200,
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["api-documentation"])
    assert result.output.strip() == json.dumps(json_documentation)


@responses.activate
def test_metadata_geography(geography_json: JSONDict, monkeypatch: MonkeyPatch) -> None:
    """Test cli geography resources."""
    monkeypatch.setattr(hexpy, "login", fake_login)

    responses.add(
        responses.GET,
        HexpySession.ROOT + "geography/info/all",
        json=geography_json,
        status=200,
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["metadata", "geography"])
    assert result.output.strip() == json.dumps(geography_json)


@responses.activate
def test_stream(posts_json: JSONDict, monkeypatch: MonkeyPatch) -> None:
    """Test cli post streaming"""
    monkeypatch.setattr(hexpy, "login", fake_login)

    responses.add(
        responses.GET,
        HexpySession.ROOT + "stream/123456789/posts",
        json={"posts": posts_json, "totalPostsAvailable": 3},
        status=200,
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["stream-posts", "-m", "3", "123456789"])
    assert result.output.strip() == "\n".join([json.dumps(x) for x in posts_json])


@responses.activate
def test_upload(
    upload_items: JSONDict, monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Test cli uploading csv custom content"""

    tmp_file = tmp_path / "myfile.csv"

    item_df = UploadCollection(items=upload_items).to_dataframe()

    item_df.to_csv(tmp_file, index=False)

    monkeypatch.setattr(hexpy, "login", fake_login)

    responses.add(
        responses.POST,
        HexpySession.ROOT + "content/upload",
        json={"status": "success"},
        status=200,
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["upload", "-d", "123456789", str(tmp_file)])
    assert result.output.strip() == json.dumps({"status": "success"}, indent=4)


@responses.activate
def test_train(train_items: JSONDict, monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    """Test cli cli upload csv training posts"""
    tmp_file = tmp_path / "myfile.csv"

    item_df = TrainCollection(items=train_items).to_dataframe()

    item_df.to_csv(tmp_file, index=False)

    monkeypatch.setattr(hexpy, "login", fake_login)

    responses.add(
        responses.POST,
        HexpySession.ROOT + "monitor/train",
        json={"status": "success"},
        status=200,
    )
    responses.add(
        responses.GET,
        HexpySession.ROOT + "monitor/detail",
        json={
            "categories": [{"name": "fake_category", "id": 9_107_252_649}],
            "type": "OPINION",
        },
        status=200,
    )

    runner = CliRunner()
    result = runner.invoke(cli, ["train", str(tmp_file), "12345678"])
    assert (
        result.output.strip()
        == "Preparing to upload:\n* 2 'fake_category' posts\nSuccessfuly uploaded 2 fake_category docs!"
    )


@responses.activate
def test_results(results_json: JSONDict, monkeypatch: MonkeyPatch) -> None:
    """Test cli monitor results output"""
    monkeypatch.setattr(hexpy, "login", fake_login)

    responses.add(
        responses.GET,
        HexpySession.ROOT + "monitor/results",
        json=results_json["results"]["sentiment_and_categories"],
        status=200,
    )
    responses.add(
        responses.GET,
        HexpySession.ROOT + "monitor/volume",
        json=results_json["results"]["volume"],
        status=200,
    )
    responses.add(
        responses.GET,
        HexpySession.ROOT + "monitor/detail",
        json={
            "resultsStart": results_json["resultsStart"],
            "resultsEnd": results_json["resultsEnd"],
        },
        status=200,
    )

    runner = CliRunner()
    result = runner.invoke(
        cli, ["results", "123456789", "volume", "sentiment_and_categories"]
    )
    assert result.output.strip() == json.dumps(results_json)


def test_helpful_error_item(upload_items: List[JSONDict]) -> None:
    """Test invalid custom content item helpful error messages"""
    del upload_items[1]["author"]

    with pytest.raises(ValidationError) as e:
        collection = UploadCollection(items=upload_items)  # noqa: F841

    result = helpful_validation_error(e.value.errors())

    assert (
        result
        == """The file contained the following problems:\n\t* items - 1 - author - field required\n"""
    )


def test_helpful_error_collection(upload_items: List[JSONDict]) -> None:
    """Test duplicate item helpful erorror message"""
    upload_items[1]["url"] = upload_items[2]["url"]
    upload_items[1]["guid"] = upload_items[2]["guid"]

    with pytest.raises(ValidationError) as e:
        collection = UploadCollection(items=upload_items)  # noqa: F841

    result = helpful_validation_error(e.value.errors())

    assert (
        result
        == """The file contained the following problems:\n\t* items - Duplicate item guids detected: ['http://www.crimsonhexagon.com/post3']\n"""
    )
