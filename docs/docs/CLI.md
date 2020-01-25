path: blob/master/src/hexpy
source: hexpy.py


Hexpy Command Line Interface
=============================

This project comes with a command line script, **hexpy**, for conveniently automating several common tasks

## Helpful Workflows

* Export sample of monitor posts to a spreadsheet.
* Easily upload a spreadsheet as custom content for analysis in ForSight.
* Quickly get multiple metrics from monitor results as JSON.
* Compose powerful shell scripts with pipe-able commands such as [jq](https://stedolan.github.io/jq/), and `xargs`.

## Usage

<div class="termy">

```bash
$ hexpy
Usage: hexpy [OPTIONS] COMMAND [ARGS]...

  Command Line interface for working with Crimson Hexagon API.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  api-documentation  Get API documentation for all endpoints.
  export             Export monitor posts as json or to a spreadsheet.
  login              Get API token with username and password and save to...
  metadata           Get Metadata for account team, monitors, and geography.
  results            Get Monitor results for 1 or more metrics.
  stream-posts       Stream posts in real time, stop after a maximum of 10K.
  train              Upload spreadsheet file of training examples for...
  upload             Upload spreadsheet file as custom content.
```
</div>

See how each `hexpy` command works by running `hexpy COMMAND --help`

## Examples

Login to Crimson API with you credentials and save your token to `~/.hexpy/token.json`.
<div class="termy">

```bash
$ hexpy login --force
# Enter username: $ username@email.com
# Enter password: $ ***********
✅ Success! Saved token to ~/.hexpy/token.json
```
</div>

Get Up-to-date API documentation as an html file
<div class="termy">

```bash
$ hexpy api-documentation -o html
```
</div>

Get list of all the user's teams using [jq](https://stedolan.github.io/jq/).
<div class="termy">

```bash
$ hexpy metadata team_list \
| jq -r '.teams[] | [.name, .id] | @tsv'
123456789   some_team_1
234567891   some_team_2
345678912   some_team_3
456789123   some_team_3
...
```
</div>

Get list of monitors for a user's team using [jq](https://stedolan.github.io/jq/).
<div class="termy">

```bash
$ hexpy metadata monitor_list --team_id TEAM_ID \
| jq -r '.monitors[] | [.id, .name] | @tsv' \
| column -t -s $'\t'
123456789   sample_monitor_1
234567891   sample_monitor_2
345678912   sample_monitor_3
456789123   sample_monitor_3
...
```
</div>

Upload TSV file as `my_custom_type` with English as the language that has tab delimited columns.
<div class="termy">

```bash
$ hexpy upload spredsheet.csv --content_type my_custom_type --language en --separator '\t'
{"status": "success"}
```
</div>

Train a Opinion Monitor with using a spreadsheet of posts with labels for the predefined categories.
<div class="termy">

```bash
$ hexpy train training_data.csv MONITOR_ID
# Preparing to upload:
#   * 2 'some_category' posts
#   * 5 'other_category' posts
# ✅ Successfuly uploaded 2 fake_category docs!
# ✅ Successfuly uploaded 5 other_category docs!
```
</div>

Get word cloud data from the monitor in the specified date range using [jq](https://stedolan.github.io/jq/).
<div class="termy">

```bash
$ hexpy results MONITOR_ID word_cloud --date_range 2017-01-01 2017-02-01 | jq .
{
  "resultsStart": "2017-01-01T00:00:00",
  "resultsEnd": "2017-02-01T00:00:00",
  "results": {
    "word_cloud": {
      "data": {
        "▇": 6,
        "⚡️": 6,
        "❤": 6,
        "・": 6,
        "🌑": 6,
        "🌹": 8,
        "👀": 7,
        "👇": 9,
        "👌": 5,
        "👏": 5,
        "💀": 5,
        "💥": 18,
        "🔥": 15,
        "😂": 46,
        "😍": 15,
        "😭": 32,
        "😱": 7,
        "🤣": 19
      },
      "status": "success"
    }
  }
}
```
</div>

Get monitor volume information for each day  as a CSV using [jq](https://stedolan.github.io/jq/)
<div class="termy">

```bash
$ hexpy results MONITOR_ID volume \
| jq -r '.results.volume.volume[] | [.startDate, .numberOfDocuments] | @csv'
"2017-01-04T00:00:00",74
"2017-01-05T00:00:00",101
"2017-01-06T00:00:00",67
"2017-01-07T00:00:00",58
"2017-01-08T00:00:00",64
"2017-01-09T00:00:00",72
"2017-01-10T00:00:00",92
"2017-01-11T00:00:00",72
"2017-01-12T00:00:00",133
"2017-01-13T00:00:00",67
...
```
</div>

Export Monitor posts to excel file called `my_export.xlsx`
<div class="termy">

```bash
$ hexpy export MONITOR_ID --output_type excel --filename my_export
# ✅ Done!
```
</div>

Export Monitor posts as json and redirect to `my_export.json`
<div class="termy">

```bash
$ hexpy export MONITOR_ID --output_type json > my_export.json
```
</div>

Export posts to excel for multiple monitors in parallel from a file containing a list of monitor ids
<div class="termy">

```bash
$ cat monitor_ids.txt | xargs -n 1 -P 4 hexpy export -o excel
# ✅ Done!
# ✅ Done!
# ✅ Done!
# ✅ Done!
```
</div>

Stream 1K real-time posts to json in the terminal
<div class="termy">

```bash
$ hexpy stream-posts STREAM_ID --max_docs 1000 --output_type json
# {'url':'http://twitter.com/sample/url/1','date':'2018-06-19T07:01:22', ...}
# {'url':'http://twitter.com/sample/url/2','date':'2018-06-21T08:40:25', ...}
# {'url':'http://twitter.com/sample/url/3','date':'2018-06-19T13:50:55', ...}
# ...
```
</div>

Stream up to 10K real-time posts to a csv file with progress bar via [pv](https://www.ivarch.com/programs/pv.shtml)
<div class="termy">

```bash
$ hexpy stream-posts STREAM_ID --output_type csv --max_docs 10000 \
| pv -s 10000 -l > streamed_posts.csv
---> 100%
```
</div>