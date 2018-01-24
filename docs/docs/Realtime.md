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
list(team_id)
```
Get the Monitors which are in Proteus

#### Arguments
* team_id: Integer, The id of the team to which the listed monitors belong.

### configure
```python
configure(monitor_id)
```
Configure the Realtime evaluators for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### enable
```python
enable(monitor_id)
```
Enable Realtime Data.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### disbale
```python
disbale(monitor_id)
```
Disable Realtime Data.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### detail
```python
detail(monitor_id)
```
Get the Realtime evaluators details for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### cashtags
```python
cashtags(monitor_id, start, top)
```
Get Cashtags associated to a Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* top: Integer, The top N cashtags to retrieve.

### hashtags
```python
hashtags(monitor_id, start, top)
```
Get Hashtags associated to a Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* top: Integer, The top N hashtags to retrieve.

### retweets
```python
retweets(monitor_id)
```
Get the Realtime retweets for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.

### social_guids
```python
social_guids(monitor_id, doc_type, start, received_after) 
```
Get the Realtime social guids for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* type: String, Specifies the document type.

### tweets
```python
tweets(monitor_id, start) 
```
Get the Realtime tweets for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.

### volume
```python
volume(monitor_id, doc_type, start) 
```
Get the Realtime volume for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* type: List, specifies the document type to filter.

### volume_by_sentiment
```python
volume_by_sentiment(monitor_id, doc_type, start) 
```
Get the Realtime volume by sentiment for the Monitor.

#### Arguments
* monitor_id: Integer, the id of the monitor being requested.
* start: Integer, specifies inclusive start date in epoch seconds.
* type: String, specifies the document type to filter.