"""CLI interface for hexpy."""
import time
import json
import pandas as pd
import numpy as np
import click
import requests
import re
from halo import Halo
from getpass import getpass
from .base import ROOT
from .session import HexpySession
from .monitor import MonitorAPI
from .content_upload import ContentUploadAPI
from .streams import StreamsAPI
from .metadata import MetadataAPI
from hexpy import __version__
import pendulum
import pathlib
from typing import Sequence, Dict, Callable
from click_help_colors import HelpColorsGroup
import os


def posts_json_to_df(docs):
    """Convert post json to flattened pandas dataframe."""

    items = []

    for doc in docs:
        record = {}
        for key, val in doc.items():
            if isinstance(val, str):
                if key == "contents" or key == "title":
                    record[key] = val.replace("\n", " ").replace("\r", " ")
                else:
                    record[key] = val
            elif key.endswith("Scores") and len(val) > 0:
                category_name = key.split("Scores")[0]
                category_max_index = np.argmax([x["score"] for x in val])
                category = val[category_max_index][category_name + "Name"]
                record[category_name + "Name"] = category
            elif isinstance(val, dict):
                for subkey, subval in val.items():
                    record[key + "_" + subkey] = subval
        items.append(record)

    df = pd.DataFrame.from_records(items)
    return df


ENDPOINT_TEMPLATE = """
#### {title}
##### {description} - Category: {category}
##### `{url}` - {method}
##### Parameters
{params}
##### Response
{results}\n\n-------------------------"""


def format_parameter(param):
    if "name" in param:
        name = param["name"]
    else:
        name = "MISSING"
    param_type = param["type"]
    required = param["required"]
    description = param["description"]

    return f"* `{name}` - {description}\n\t- Type: {param_type}\n\t- Required = {required}\n"


def format_response(response):
    if "name" in response:
        name = response["name"]
    else:
        name = "MISSING"
    param_type = response["type"]
    restricted = response["restricted"]
    description = response["description"]

    return f"* `{name}` - {description}\n\t- Type: {param_type}\n\t- Restricted = {restricted}\n"


def format_endpoint(endpoint, index_num):
    title = endpoint["endpoint"]
    url = endpoint["url"]
    method = endpoint["method"]
    description = endpoint["description"]
    category = endpoint["category"]
    params = "".join([format_parameter(param) for param in endpoint["parameters"]])
    results = "".join([format_response(r) for r in endpoint["response"]])

    return ENDPOINT_TEMPLATE.format(
        title=title,
        url=url,
        method=method,
        description=description,
        category=category,
        params=params,
        results=results,
    )


def docs_to_text(json_docs, mode="markdown"):
    endpoints = json_docs["endpoints"]
    doc = f"# Crimson Hexagon API Documenttion\n**ROOT_URL = `{ROOT}`**\n\n### Endpoints\n"

    for i, e in enumerate(endpoints):

        if mode == "md":
            anchor = e["endpoint"].lower().replace("-", " ")
            anchor = re.sub(r"\s+", "-", anchor)
        elif mode == "gfm":
            anchor = "user-content-" + e["endpoint"].lower().replace(" ", "-")
        else:
            raise click.ClickException("Invalid markdown mode")
        doc += f"* [{e['endpoint']}](#{anchor})\n"

    return doc + "\n".join([format_endpoint(e, i) for i, e in enumerate(endpoints)])


@click.group(
    cls=HelpColorsGroup, help_headers_color="blue", help_options_color="yellow"
)
@click.version_option(version=__version__)
def cli():
    """Command Line interface for working with Crimson Hexagon API."""
    pass


@cli.command()
@click.option(
    "--force/--no-force",
    "-f",
    default=False,
    help="force signing in again and storing token",
)
@click.option(
    "--expiration/--no-expiration",
    "-e",
    default=True,
    help="Get token valid for 24 hours, or with no expiration",
)
def login(force: bool = False, expiration: bool = True) -> HexpySession:
    """Session login credentials."""
    try:
        if not force:
            session = HexpySession.load_auth_from_file()
            return session
        else:
            raise IOError
    except IOError:
        username = input("Enter username: ")
        password = getpass(prompt="Enter password: ")
        session = HexpySession.login(username, password, no_expiration=not expiration)
        session.save_token()
        spinner = Halo(text="Success!", spinner="dots")
        spinner.succeed()
        return session


@cli.command()
@click.option(
    "--date_range",
    "-d",
    nargs=2,
    default=None,
    help="start and end date of export in YYYY-MM-DD format.",
)
@click.argument("monitor_id", type=int)
@click.argument("metrics", nargs=-1)
@click.pass_context
def results(
    ctx, monitor_id: int, metrics: Sequence[str], date_range: Sequence[str] = None
) -> None:
    """Get Monitor results for 1 or more metrics.

    \b
    Valid metrics
        * volume
        * word_cloud
        * top_sources
        * interest_affinities
        * sentiment_and_categories
    """

    session = ctx.invoke(login, expiration=True, force=False)
    client = MonitorAPI(session)
    if date_range:
        results = client.aggregate(monitor_id, date_range, list(metrics))
    else:
        details = client.details(monitor_id)
        start = details["resultsStart"]
        end = details["resultsEnd"]
        results = client.aggregate(monitor_id, [(start, end)], list(metrics))
    click.echo(json.dumps(results[0]["results"][0], ensure_ascii=False))


@cli.command()
@click.option("--team_id", "-t", default=None, help="team id for monitor list")
@click.option(
    "--country", "-c", default=None, help="country code for city or state geo"
)
@click.option("--monitor_id", "-m", default=None, help="monitor id for details")
@click.argument("info", type=str)
@click.pass_context
def metadata(
    ctx, info: str, team_id: int = None, country: str = None, monitor_id: int = None
) -> None:
    """Get Metadata for account team, monitors, and geography.

    \b
    Valid info
        * team_list
        * monitor_list
        * geography
        * states
        * cities
        * countries
        * monitor_details
        * stream_list
    """

    session = ctx.invoke(login, expiration=True, force=False)
    client = MetadataAPI(session)
    monitor_client = MonitorAPI(session)
    stream_client = StreamsAPI(session)
    metadata: Dict[str, Callable] = {
        "team_list": client.team_list,
        "monitor_list": client.monitor_list,
        "geography": client.geography,
        "states": client.states,
        "cities": client.cities,
        "countries": client.countries,
        "monitor_details": monitor_client.details,
        "stream_list": stream_client.stream_list,
    }
    if team_id:
        return click.echo(json.dumps(metadata[info](team_id=team_id)))
    elif country:
        return click.echo(json.dumps(metadata[info](country=country)))
    elif monitor_id:
        return click.echo(json.dumps(metadata[info](monitor_id=monitor_id)))
    else:
        return click.echo(json.dumps(metadata[info]()))


@cli.command()
@click.option(
    "--output_type",
    "-o",
    type=click.Choice(["markdown", "html", "json"]),
    default="json",
    help="file type of export. (default=json)",
)
@click.pass_context
def api_documentation(ctx, output_type: str = "json"):
    """Get API documentation for all endpoints.

    \b
    output types
        * JSON (default)
        * Markdown File
        * HTML File
    """
    session = ctx.invoke(login, expiration=True, force=False)
    client = MetadataAPI(session)
    json_docs = client.api_documentation()
    if output_type == "json":
        click.echo(json.dumps(json_docs))
        return
    if output_type == "markdown":
        md = docs_to_text(json_docs, "md")
        with open("crimson_api_docs.md", "w") as outfile:
            outfile.write(md)
    else:
        md = docs_to_text(json_docs, "gfm")
        html = requests.post(
            "https://api.github.com/markdown",
            data=json.dumps({"text": md, "mode": "markdown"}),
        ).text
        path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        with open(path / "head.html") as infile:
            html = infile.read() + html + "</article></body></html>"
        with open("crimson_api_docs.html", "w") as outfile:
            outfile.write(html)


@cli.command()
@click.argument("filename")
@click.option(
    "--content_type",
    "-c",
    default=None,
    help="Custom content type, as specified in Forsight.",
)
@click.option("--delimiter", "-d", default=",", help="CSV column delimiter.")
@click.option("--language", "-l", default="en", help="language code of documents")
@click.pass_context
def upload(
    ctx,
    filename: str,
    content_type: str = None,
    delimiter: str = ",",
    language: str = "en",
) -> None:
    """Upload spreadsheet file as custom content."""

    if delimiter == "\\t":
        delimiter = "\t"
    session = ctx.invoke(login, expiration=True, force=False)
    client = ContentUploadAPI(session)
    if filename.endswith(".csv"):
        items = pd.read_csv(filename, sep=delimiter)
    elif filename.endswith(".xlsx"):
        items = pd.read_excel(filename)
    else:
        raise click.ClickException("File type must be either .csv or .xlsx")

    # Handle Content Types
    if content_type is not None:
        items["type"] = content_type
    elif "type" not in items.columns:
        raise click.ClickException("Missing custom content type")

    # Handle titles
    if "title" not in items.columns:
        items["title"] = [f"Post {i}" for i in range(len(items))]

    # Handle language code
    if "language" not in items.columns:
        items["language"] = language

    # Correctly format dates
    try:
        dates = [pendulum.parse(x).to_iso8601_string() for x in items["date"]]
    except Exception as e:
        raise click.ClickException(
            """Could not parse date format.  Must be Year-Month-Day as in 2017-10-01.
            Optionally include time as 2017-10-01T21:30:05
            """
        )

    items.loc[:, "date"] = dates

    # Check for required fields
    try:
        assert {
            "contents",
            "date",
            "author",
            "language",
            "type",
            "title",
            "url",
        }.issubset(set(items.columns))
    except AssertionError:
        raise click.ClickException(
            "1 or more missing fields.  Required fields: contents, date, author, language, type, title, url"
        )

    # Assert Unique Urls
    try:
        assert len(items[items.url.duplicated()]) == 0
    except AssertionError:
        raise click.ClickException("Duplicate URLs detected.")

    # Covert data to list of dictionaries
    data = items[
        ["title", "date", "contents", "type", "language", "author", "url"]
    ].to_dict(orient="records")

    # TODO Handle Geography
    if "geography" in items.columns:
        pass

    response = client.upload(data=data)
    click.echo(json.dumps(response))
    spinner = Halo(text="Success!", spinner="dots")
    spinner.succeed()


@cli.command()
@click.argument("monitor_id", type=int)
@click.option(
    "--limit/--no-limit",
    "-l",
    default=True,
    help="Limit export to 500 posts or extend to 10K. (default=limit)",
)
@click.option(
    "--output_type",
    "-o",
    type=click.Choice(["csv", "excel", "json"]),
    default="csv",
    help="file type of export. (default=csv)",
)
@click.option(
    "--dates",
    "-d",
    nargs=2,
    default=None,
    help="start and end date of export in YYYY-MM-DD format.",
)
@click.option(
    "--filename", "-f", default=None, help="filename. Default is monitor name."
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="CSV column delimiter in quotes.(default=',')",
)
@click.pass_context
def export(
    ctx,
    monitor_id: int,
    limit: bool = True,
    dates: Sequence[str] = None,
    output_type: str = "csv",
    filename: str = None,
    delimiter: str = ",",
) -> None:
    """Export monitor posts as json or to a spreadsheet."""

    if delimiter == "\\t":
        delimiter = "\t"
    session = ctx.invoke(login, expiration=True, force=False)
    client = MonitorAPI(session)
    details = client.details(monitor_id)
    info = details["name"]
    if dates:
        docs = client.posts(monitor_id, dates[0], dates[1], extend_limit=not limit)[
            "posts"
        ]
    else:
        start = details["resultsStart"]
        end = details["resultsEnd"]
        docs = client.posts(monitor_id, start, end, extend_limit=not limit)["posts"]

    if output_type == "json":
        for p in docs:
            click.echo(json.dumps(p, ensure_ascii=False))
    else:
        df = posts_json_to_df(docs)

        if filename:
            name = filename
        else:
            name = f"{monitor_id}_{info.replace(' ', '_')}_Posts"
        if output_type == "csv":
            df.to_csv(name + ".csv", index=False, sep=delimiter)
        elif output_type == "excel":
            df.to_excel(name + ".xlsx", index=False)
        else:
            raise click.ClickException("Output type must be either csv, excel or json")
        spinner = Halo(text="Done!", spinner="dots")
        spinner.succeed()


@cli.command()
@click.argument("stream_id", type=int)
@click.option(
    "--stop_after",
    "-s",
    type=int,
    default=100,
    help="Stop streaming after number of posts reached. (default=100)",
)
@click.option(
    "--output_type",
    "-o",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="type of data to output. (default=json)",
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="CSV column delimiter in quotes.(default=',')",
)
@click.pass_context
def stream_posts(
    ctx,
    stream_id: int,
    stop_after: int = 100,
    output_type: str = "json",
    delimiter: str = ",",
):
    """Stream posts in real time, stop after a maximum of 10K."""

    if delimiter == "\\t":
        delimiter = "\t"
    session = ctx.invoke(login, expiration=True, force=False)
    client = StreamsAPI(session)
    so_far = 0
    request_count = 0
    first_fetch = True
    if stop_after > 10000:
        stop_after = 10000
    while so_far < stop_after and request_count < 10000:
        request_count += 1
        response = client.posts(stream_id)
        posts = response["posts"]
        so_far += len(posts)
        if output_type == "json":
            for p in posts:
                click.echo(json.dumps(p, ensure_ascii=False))
        elif output_type == "csv":
            df = posts_json_to_df(posts)
            if first_fetch:
                click.echo(df.to_csv(sep=delimiter, index=False).strip())
                first_fetch = False
            else:
                click.echo(df.to_csv(header=None, sep=delimiter, index=False).strip())
        else:
            raise click.ClickException("Output type must be either csv or json")
        if response["totalPostsAvailable"] == 0:
            time.sleep(.6)


if __name__ == "__main__":
    cli()
