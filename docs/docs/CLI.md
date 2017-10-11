Hexpy Command Line Interface
=============================

**hexpy** comes with an optional console script for conveniently automating several common tasks

## Helpful Commands

* Export sample of monitor posts to a spreadsheet.
* Easily upload a spreadsheet as custom content for analysis in ForSight.
* Quickly get multiple metrics from monitor results as JSON. (Works well with [jq](https://stedolan.github.io/jq/))


## Installation
<!-- To install the most recent stable release run `pip install hexpy`. -->

To install the optional console command:
```bash
$ pip install git+git://github.com/sullivancolin/hexpy.git@master[cli]
```
 or
```bash
$ git clone https://github.com/sullivancolin/hexpy.git
$ pip install hexpy/[cli]
```

## Usage

### Basic
```
$ hexpy [OPTIONS] COMMAND [ARGS]...
```

### Commands
* **export**  Save Monitor posts as spreadsheet.
* **query**   Get Monitor results for 1 or more metrics.
* **upload**  Upload spreadsheet file as custom content.

See how each `hexpy` command works by running `hexpy COMMAND --help`

## Examples

Export Monitor posts to excel file called `my_export.xlsx`
```bash
$ hexpy export MONITOR_ID --file_type excel --output my_export
```

Upload CSV file as `my_custom_types` with English language code and column delimiter is tab
```bash
$ hexpy upload spredsheet.csv --content_type my_custom_type --language en --delimiter '\t'
```

Get word cloud and volume information from the monitor in the specified date range
```bash
$ hexpy query MONITOR_ID volume word_cloud --date_range 2017-01-01 2017-02-01
```

Get volume information for the monitor and get count for each day
```bash
$ hexpy query MONITOR_ID volume | jq -c -r '.results.volume.volumes[] | [.startDate, .numberOfDocuments]
["2017-01-04T00:00:00",74]
["2017-01-05T00:00:00",101]
["2017-01-06T00:00:00",67]
["2017-01-07T00:00:00",58]
["2017-01-08T00:00:00",64]
["2017-01-09T00:00:00",72]
["2017-01-10T00:00:00",92]
["2017-01-11T00:00:00",72]
["2017-01-12T00:00:00",133]
["2017-01-13T00:00:00",67]
["2017-01-14T00:00:00",68]
["2017-01-15T00:00:00",72]
...'
```