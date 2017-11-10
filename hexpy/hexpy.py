# -*- coding: utf-8 -*-
"""CLI interface for hexpy."""
from datetime import datetime
import time
import json
import pandas as pd
import numpy as np
import click
from halo import Halo
from getpass import getpass
from clint.textui import progress
from .auth import HexpyAuthorization
from .monitor import MonitorAPI
from .content_upload import ContentUploadAPI
from .analysis import AnalysisAPI


@click.group()
def cli():
    """Command Line interface for working with Crimson Hexagon API."""
    pass


@cli.command()
@click.option(
    "--force/--no-force",
    '-f',
    default=False,
    help="force signing in again and storing token")
@click.option(
    '--expiration/--no-expiration',
    '-e',
    default=True,
    help='Get token valid for 24 hours, or with no expiration')
def login(force, expiration):
    """Get valid authorization from user."""
    try:
        if not force:
            auth = HexpyAuthorization.load_auth_from_file()
            return auth
        else:
            raise IOError
    except IOError:
        username = input('Enter username: ')
        password = getpass(prompt='Enter password: ')
        auth = HexpyAuthorization(username, password, no_expiration=expiration)
        auth.save_token()
        spinner = Halo(text='Success!', spinner='dots')
        spinner.succeed()
        return auth


@cli.command()
@click.option(
    '--date_range',
    '-d',
    nargs=2,
    default=None,
    help='start and end date of export in YYYY-MM-DD format.')
@click.argument('monitor_id', type=int)
@click.argument('metrics', nargs=-1)
@click.pass_context
def results(ctx, monitor_id, metrics, date_range):
    """Get Monitor results for 1 or more metrics.

    \b
    Valid metrics
        * volume
        * word_cloud
        * top_sources
        * interest_affinities
        * sentiment_and_categories
    """
    auth = ctx.invoke(login, expiration=True, force=False)
    client = MonitorAPI(auth)
    details = client.details(monitor_id)
    if date_range:
        results = client.aggregate(monitor_id, date_range, list(metrics))
    else:
        start = details["resultsStart"]
        end = details["resultsEnd"]
        results = client.aggregate(monitor_id, [(start, end)], list(metrics))
    click.echo(
        json.dumps(results[0]["results"][0], indent=4, ensure_ascii=False))


@cli.command()
@click.argument('filename')
@click.option(
    '--content_type',
    '-c',
    default=None,
    help='Custom content type, as declared in Forsight.')
@click.option('--delimiter', '-d', default=",", help='CSV column delimiter.')
@click.option(
    '--language', '-l', default="en", help='language code of documents')
@click.pass_context
def upload(ctx, filename, content_type, delimiter, language):
    """Upload spreadsheet file as custom content."""
    auth = ctx.invoke(login, expiration=True, force=False)
    client = ContentUploadAPI(auth)
    if filename.endswith(".csv"):
        items = pd.read_csv(filename, sep=delimiter)
    elif filename.endswith(".xlsx"):
        items = pd.read_excel(filename)
    else:
        raise ValueError("File type must be either .csv or .xlsx")

    # Handle Content Types
    if content_type is not None:
        items["type"] = content_type
    elif "type" not in items.columns:
        raise ValueError("missing custom content type")

    # Handle titles
    if "title" not in items.columns:
        items["title"] = ["Post {}".format(i) for i in range(len(items))]

    # Handle language code
    if "language" not in items.columns:
        items["language"] = language

    # Correctly format dates
    try:
        dates = [
            datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").isoformat()
            for x in items["date"]
        ]
    except:
        try:
            dates = [
                datetime.strptime(x, "%Y-%m-%d").isoformat()
                for x in items["date"]
            ]
        except:
            raise ValueError(
                """Could not parse date format.  Must be Year-Month-Day as in 2017-10-01.
                Optionally include time as 2017-10-01T21:30:05
                """)

    items.loc[:, "date"] = dates

    # Check for required fields
    assert ({"contents", "date", "author", "language", "type",
             "title"}.issubset(set(items.columns)))

    # Covert data to list of dictionaries
    data = items[[
        "title", "date", "contents", "type", "language", "author", "url"
    ]].to_dict(orient='records')

    # TODO Handle Geography
    if "geography" in items.columns:
        pass

    response = client.upload(data=data)
    print(response)
    spinner = Halo(text='Success!', spinner='dots')
    spinner.succeed()


@cli.command()
@click.argument('monitor_id', type=int)
@click.option(
    '--limit/--no-limit',
    '-l',
    default=True,
    help='Limit export to 500 posts or extend to 10K.')
@click.option(
    '--file_type',
    '-f',
    type=click.Choice(['csv', 'excel']),
    default="csv",
    help='file type of export.')
@click.option(
    '--dates',
    '-d',
    nargs=2,
    default=None,
    help='start and end date of export in YYYY-MM-DD format.')
@click.option(
    '--output',
    '-o',
    default=None,
    help='output filename. Default is monitor name.')
@click.option('--delimiter', '-d', default=",", help='CSV column delimiter.')
@click.pass_context
def export(ctx, monitor_id, limit, dates, file_type, output, delimiter):
    """Save Monitor posts as spreadsheet."""
    if delimiter == "\\t":
        delimiter = '\t'
    auth = ctx.invoke(login, expiration=True, force=False)
    client = MonitorAPI(auth)
    details = client.details(monitor_id)
    info = details["name"]
    if dates:
        docs = client.posts(
            monitor_id, dates[0], dates[1], extend_limit=not limit)["posts"]
    else:
        start = details["resultsStart"]
        end = details["resultsEnd"]
        docs = client.posts(
            monitor_id, start, end, extend_limit=not limit)["posts"]

    items = []

    for doc in progress.bar(docs):
        record = {}
        for key, val in doc.items():
            if isinstance(val, str):
                if key == "contents" or key == "title":
                    record[key] = val.replace("\n", " ").replace("\r", " ")
                else:
                    record[key] = val
            elif key.endswith("Scores"):
                category_name = key.split("Scores")[0]
                category_max_index = np.argmax([x["score"] for x in val])
                category = val[category_max_index][category_name + "Name"]
                record[category_name + "Name"] = category
            elif isinstance(val, dict):
                for subkey, subval in val.items():
                    record[key + "_" + subkey] = subval
        items.append(record)

    df = pd.DataFrame.from_records(items)
    df = df.set_index('date')
    df = df.sort_index(ascending=False)
    if output:
        info = output
    else:
        info = "{}_{}_Posts".format(monitor_id, info.replace(" ", "_"))
    if file_type == "csv":
        df.to_csv(info + ".csv", index=True, sep=delimiter)
    else:
        df.to_excel(info + ".xlsx", index=True)
    spinner = Halo(text='Done!', spinner='dots')
    spinner.succeed()


@cli.command()
@click.argument('query_file')
@click.pass_context
def query(ctx, query_file):
    """Submit a query task on 24 hours of data."""
    auth = ctx.invoke(login, expiration=True, force=False)
    client = AnalysisAPI(auth)
    query_json = json.load(open(query_file))
    response = client.analysis_request(query_json)
    if response["status"] == "WAITING":
        request_id = response["resultId"]
        results = client.results(request_id)
        while results["status"] == "WAITING":
            time.sleep(10)
            results = client.results(request_id)
    else:
        results = response
    click.echo(json.dumps(results, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    cli()