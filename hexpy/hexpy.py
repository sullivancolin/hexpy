# -*- coding: utf-8 -*-
"""CLI interface for hexpy."""
from collections import defaultdict
import pandas as pd
import numpy as np
import click
from getpass import getpass
from clint.textui import progress
from .auth import CrimsonAuthorization
from .monitor import MonitorAPI
from .content_upload import ContentUploadAPI


def get_auth():
    try:
        auth = CrimsonAuthorization.load_auth_from_file()
        return auth
    except IOError:
        username = input('Enter username: ')
        password = getpass(prompt='Enter password: ')
        auth = CrimsonAuthorization(username, password, no_expiration=False)
        return auth


@click.group()
def cli():
    """Top level function for command line interface."""
    pass


@cli.command()
def upload():
    pass


@cli.command()
@click.argument('monitor_id')
@click.option('--limit/--no-limit', '-l', default=True)
@click.option(
    '--file_type', '-f', type=click.Choice(['csv', 'excel']), default="csv")
@click.option('--dates', '-d', nargs=2, default=None)
@click.option('--output', '-o', default=None)
def export(monitor_id, limit, dates, file_type, output):
    auth = get_auth()
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
        df.to_csv(info + ".csv", index=True)
    else:
        df.to_excel(info + ".xlsx", index=True)


if __name__ == '__main__':
    cli()