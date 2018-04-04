A Python Client for the Crimson Hexagon API
===========================================

**hexpy** is a simple python package for working with the Crimson Hexagon API

## Why use this client?

* Easily and securely manage account authentication.
* Automatically abide by Crimson Hexagon's rate limits.
* Automatically convert python data to/from JSON strings.
* Automatically check requests success.
* Make it easy to do common tasks like exporting and uploading content.
* Easily create shell scripts to work with API data.

## Requirements
**hexpy** is compatible with Python 3.5 and higher

## Installation
To install the most recent stable release run `pip install hexpy`.

To install the latest version:
```bash
$ git clone https://github.com/sullivancolin/hexpy.git
$ pip install hexpy/
```

## Project Homepage

Visit [Github](https://github.com/sullivancolin/hexpy) project page for full source code.

## Quickstart

```python
>>> from hexpy import HexpyAuthorization, MonitorAPI
>>> auth = HexpyAuthorization(username="user@email.com", password="crimson_login")
>>> monitor_results_client=MonitorAPI(auth)
>>> monitor_results_client.details(MONITOR_ID)
{'categories': [{'hidden': False,
   'id': 6054759055,
   'name': 'Basic Positive',
   'sortOrder': 100,
   'status': 'red',
   'trainingDocs': 0},
  {'hidden': False,
   'id': 6054759059,
   'name': 'Basic Neutral',
   'sortOrder': 101,
   'status': 'red',
   'trainingDocs': 0},
  {'hidden': False,
   'id': 6054759051,
   'name': 'Basic Negative',
   'sortOrder': 102,
   ...
```
