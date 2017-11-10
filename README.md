A Python Client for the Crimson Hexagon API
===================

**hexpy** is a simple python package for working with the Crimson Hexagon API

## Why use this client?

* Easily and securely manage account authentication.
* Automatically abides by Crimson Hexagon's rate limits.
* Automatically converts python data to/from JSON strings.
* Automatically check for request errors.
* Easily create shell scripts to work with API data

## Installation
<!-- To install the most recent stable release run `pip install hexpy`. -->

To install the latest version:
```bash
$ pip install git+git://github.com/sullivancolin/hexpy.git@master
```
 or
```bash
$ git clone https://github.com/sullivancolin/hexpy.git
$ pip install -e hexpy/
```

## Project Homepage

Visit [Github](https://github.com/sullivancolin/hexpy) project page for full source code.

## Example Usage

```python
>>> from hexpy import CrimsonAuthorization, MonitorAPI
>>> auth = CrimsonAuthorization(username="user@email.com", password="crimson_login")
>>> monitor_results_client=MonitorAPI(auth)
>>> monitor.details(monitor_id)
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