Streams API
===========

## Class for working with Realtime Streams API.

## Example usage.

```python
>>> from hexpy import HexpySession , StreamsAPI
>>> session = HexpySession.load_auth_from_file()
>>> streams_client = StreamsAPI(session)
>>> streams_client.stream_list(team_id)
>>> session.close()
```

## Methods

### posts
```python
posts(stream_id, count=100)
```
Return posts from a stream.

#### Arguments:
* stream_id: Integer, the id of the stream containing the posts, available via the stream list endpoint
* count: Integer, the count of posts to retrieve from the stream, max = 100

### stream_list
```python
stream_list(team_id)
```
List all available Realtime Streams for a team.

#### Arguments
* team_id: Integer the id of the team, available via the team list endpoint

