path: blob/master/hexpy/src
source: streams.py

Streams API
===========

Class for working with Streams API.

## Example usage

```python
>>> from hexpy import HexpySession , StreamsAPI
>>> session = HexpySession.load_auth_from_file()
>>> streams_client = StreamsAPI(session)
>>> streams_client.stream_list(team_id)
```

## Methods

### posts
```python
posts(stream_id: int, count: int = 100) -> JSONDict
```
Return posts from a stream.

#### Arguments:
* stream_id: Integer, the id of the stream containing the posts.
* count: Integer, the count of posts to retrieve from the stream, max = 100.

### stream_list
```python
stream_list(team_id: int) -> JSONDict
```
List all available Streams for a team.

#### Arguments
* team_id: Integer the id of the team.

### create_stream
```python
create_stream(team_id: int, name: str) -> JSONDict
```
Create new stream for a team. System Admin Only.

#### Arguments
* team_id: Integer, the id of the team to associate created stream with.
* name: String, the name to associate with the newly created stream.

### delete_stream
```python
delete_stream(stream_id: int) -> JSONDict
```
Delete a stream. System Admin Only.

#### Arguments
* stream_id: Integer, the id of the stream to be deleted.

### add_monitor_to_stream
```python
add_monitor_to_stream(stream_id: int, monitor_id: int) -> JSONDict
```
Associate a monitor with a stream. System Admin Only.

#### Arguments
* stream_id: Integer, the id of stream to be modified.
* monitor_id: Integer, the id to be associated with the stream.

### remove_monitor_from_stream
```python
remove_monitor_from_stream(stream_id: int, monitor_id: int) -> JSONDict
```
Remove association between monitor and stream.  System Admin Only.

#### Arguments
* stream_id: Integer, the id of stream to be updated.
* monitor_id: Integer, the id to be removed from the stream.

### update_stream
```python
update_stream(stream_id: int, name: str) -> JSONDict
```
Update name of stream. System Admin Only.

#### Arguments
* stream_id: Integer, the id of stream to be updated.
* name: String, the new name to be associated with the stream.