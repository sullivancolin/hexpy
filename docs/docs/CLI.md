Hexpy Command Line Interface
=============================

This project comes with a command line script, **hexpy**, for conveniently automating several common tasks

## Helpful Workflows

* Export sample of monitor posts to a spreadsheet.
* Easily upload a spreadsheet as custom content for analysis in ForSight.
* Quickly get multiple metrics from monitor results as JSON. 
* Compose powerful shell scripts with pipe-able commands such as [jq](https://stedolan.github.io/jq/), and `xargs`.

## Usage

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

See how each `hexpy` command works by running `hexpy COMMAND --help`

## Examples

Login to Crimson API with you credentials and save your token to `~/.hexpy/token.json`.
```bash
$ hexpy login --force
Enter username: username@email.com
Enter password: ***********
Success! Saved token to ~/.hexpy/token.json
```

Get Up-to-date API documentation as an html file
```bash
$ hexpy api-documentation -o html
```

Get list of all the user's teams using [jq](https://stedolan.github.io/jq/).
```bash
$ hexpy metadata team_list | jq -r '.teams[] | [.name, .id] | @tsv' | column -t -s $'\t'
```

Get list of monitors for a user's team using [jq](https://stedolan.github.io/jq/).
```bash
$ hexpy metadata monitor_list --team_id TEAM_ID | jq -r '.monitors[] | [.id, .name] | @tsv' | column -t -s $'\t'
```

Upload TSV file as `my_custom_type` with English as the language that has tab delimited columns.
```bash
$ hexpy upload spredsheet.csv --content_type my_custom_type --language en --separator '\t'
```

Train a Opinion Monitor with using a spreadsheet of posts with labels for the predefined categories.
```bash
$ hexpy train training_data.csv MONITOR_ID
```

Get word cloud and volume information from the monitor in the specified date range.
```bash
$ hexpy results MONITOR_ID volume word_cloud --date_range 2017-01-01 2017-02-01
```

Get monitor volume information for each day  as a CSV using [jq](https://stedolan.github.io/jq/)
```bash
$ hexpy results MONITOR_ID volume | jq -r '.results.volume.volume[] | [.startDate, .numberOfDocuments] | @csv'
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

Export Monitor posts to excel file called `my_export.xlsx`
```bash
$ hexpy export MONITOR_ID --output_type excel --filename my_export
```

Export Monitor posts as json and redirect to `my_export.json`
```bash
$ hexpy export MONITOR_ID --output_type json > my_export.json
```

Export posts to excel for multiple monitors in parallel from a file containing a list of monitor ids
```bash
$ cat monitor_ids.txt | xargs -n 1 -P 4 hexpy export -o excel
```

Stream 1K real-time posts to json in the terminal
```bash
$ hexpy stream-posts STREAM_ID --max_docs 1000 --output_type json 
```

Stream up to 10K real-time posts to a csv file with tab delimiter 
```bash
$ hexpy stream-posts STREAM_ID --output_type csv --max_docs 10000 --separator '\t' | pv -s 10000 -l > streamed_posts.csv
```
