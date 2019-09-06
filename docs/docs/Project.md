path: blob/master/src/hexpy
source:  project.py

Project
===============

Hybrid [Pydantic Style Class](https://pydantic-docs.helpmanual.io/) and [MonitorAPI](Monitor.md) to make working with a monitor results more convenient.

## `Project`
Class for working with a Crimson Hexagon Monitor Project.

Possesses all the same methods as [MonitorAPI](Monitor.md) with default arguments of the project `monitor_id`, `start`, and `end`.

### Attributes
* id: Integer
* name: String
* description: String
* type: Choice of BUZZ/OPINION/SOCIAL
* enabled: Boolean
* resultsStart: DateTime
* resultsEnd: DateTime
* keywords: String
* languages: JSONDict
* geolocations: JSONDict
* gender: Optional M/F/None
* sources: List of Strings
* timezone: String
* teamName: String
* tags: List of Strings
* subfilters: List of dictionaries
* categories: List of dictionaries
* emotions: List of dictionaries
* session: HexpySession
* days: List of Date Strings in the monitor

### Example usage.

```python
>>> from hexpy import HexpySession, Project
>>> session = HexpySession.load_auth_from_file()
>>> project = Project.get_from_monitor_id(session, monitor_id=123456789)
>>> description = project.description
>>> start = project.resultsStart
>>> end = project.resultsEnd
### get sample of posts over default date range in the project
>>> sample_posts = project.posts()
### get monitor results for each day in the project overriding default date range
>>> for day1, day2 in zip(project, project[1:]):
        word_cloud_results = project.word_cloud(start=day1, end=day2)
```

### Methods

### get_from_monitor_id
```python
get_from_monitor_id(session: HexpySession, monitor_id: int) -> Project
```
Instantiate from session and Monitor ID

#### Arguments
* session: HexpySession object
* monitor_id: Integer for Monitor to work with


### **All other methods of [MonitorAPI](Monitor.md#methods) are available using default `monitor_id`, `start`, and `end`**