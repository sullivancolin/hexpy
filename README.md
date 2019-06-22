<p align="center">
  <a href="https://sullivancolin.github.io/hexpy/"><img src="https://sullivancolin.github.io/hexpy/images/banner.png" alt="hexpy"></a>
</p>
<p align="center">
<a href="https://travis-ci.com/sullivancolin/hexpy" target="_blank">
    <img src="https://travis-ci.com/sullivancolin/hexpy.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/sullivancolin/hexpy" target="_blank">
    <img src="https://codecov.io/gh/sullivancolin/hexpy/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/hexpy/" target="_blank">
    <img src="https://badge.fury.io/py/hexpy.svg" alt="PyPI version">
</a>
</p>

A Python Client for the Crimson Hexagon API
===========================================

**hexpy** is a simple python package for working with the [Crimson Hexagon API](https://apidocs.crimsonhexagon.com/)

---
## Project Homepage

**Documentation**: [hexpy](https://sullivancolin.github.io/hexpy/)

**Source Code**: [Github](https://github.com/sullivancolin/hexpy)

---

## Why use this client?

* Easily and securely manage account authentication.
* Automatically abide by Crimson Hexagon's rate limits.
* Automatically convert python data to/from JSON strings.
* Automatically check requests success.
* Make it easy to do common tasks like exporting and uploading content.
* Easily create shell scripts to work with API data.

## Requirements
**hexpy** is compatible with Python 3.6 and higher

## Installation
To install the most recent stable release run `pip install hexpy`.

To install the latest version:
```bash
$ git clone https://github.com/sullivancolin/hexpy.git
$ pip install hexpy/
```

## Quick Start

```python
>>> from hexpy import HexpySession, MonitorAPI
>>> session = HexpySession.login(username="user@email.com", password="crimson_login")
>>> monitor_results_client = MonitorAPI(session)
>>> monitor_results_client.details(monitor_id)
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
}
```