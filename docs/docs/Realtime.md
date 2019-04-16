path: blob/master/hexpy
source: realtime.py

Realtime API
===========

## Class for working with Realtime Results API.

## Example usage.

```python
>>> from hexpy import HexpySession, RealtimeAPI
>>> session = HexpySession.load_auth_from_file()
>>> realtime_client = RealtimeAPI(session)
>>> realtime_client.list(team_id)
>>> session.close()
```

## Methods

### list
```python
list(team_id: int) -> Dict[str, Any]
```
Get the Monitors which are in Proteus

#### Arguments
* team_id: Integer, The id of the team to which the listed monitors belong.

### configure
```python
configure(monitor_id: int) -> Dict[str, Any]
```
Configure the Realtime evaluators for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### enable
```python
enable(monitor_id: int) -> Dict[str, Any]
```
Enable Realtime Data.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### disbale
```python
disbale(monitor_id: int) -> Dict[str, Any]
```
Disable Realtime Data.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### detail
```python
detail(monitor_id: int) -> Dict[str, Any]
```
Get the Realtime evaluators details for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### cashtags
```python
cashtags(monitor_id: int, start: int = None, top: int = None) -> Dict[str, Any]
```
Get Cashtags associated to a Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* top: Integer, The top N cashtags to retrieve.

### hashtags
```python
hashtags(monitor_id: int, start: int = None, top: int = None) -> Dict[str, Any]
```
Get Hashtags associated to a Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* top: Integer, The top N hashtags to retrieve.

### retweets
```python
retweets(monitor_id: int) -> Dict[str, Any]
```
Get the Realtime retweets for the Monitor.

### full_retweets
```python
full_retweets(monitor_id: int, start: int = None) -> Dict[str, Any]
```
Get the Realtime fullretweets for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### social_guids
```python
social_guids(monitor_id: int, doc_type: str, start: int = None, received_after: int = None) -> Dict[str, Any]
```
Get the Realtime social guids for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* doct_type: String, Specifies the document type.
* start: Integer, specifies inclusive start date in epoch seconds.
* received_after: Integer, Specifies inclusive received after date in epoch seconds.
* maxresults: Integer, Specifies maximum results to fetch.

### tweets
```python
tweets(monitor_id: int, start: int = None) -> Dict[str, Any]
```
Get the Realtime tweets for the Monitor.

### full_tweets
```python
full_tweets(monitor_id: int, start: int = None) -> Dict[str, Any]
```
Get the Realtime fulltweets for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.

### volume
```python
volume(monitor_id: int, start: int = None, doc_type: List = None) -> Dict[str, Any]
```
Get the Realtime volume for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* doc_type: List, specifies the document type to filter.

### volume_by_sentiment
```python
volume_by_sentiment(monitor_id: int, start: int, doc_type: str) -> Dict[str, Any]
```
Get the Realtime volume by sentiment for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* doc_type: String, specifies the document type to filter.

### volume_by_emotion
```python
volume_by_emotion(monitor_id: int, start: int, doc_type: str) -> Dict[str, Any]
```
Get the Realtime volume by emotion for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* doc_type: String, specifies the document type to filter.
