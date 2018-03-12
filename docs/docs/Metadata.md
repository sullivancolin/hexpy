Metadata API
============

## Class for working with Crimson Hexagon account and analysis metadata.

## Example usage.

```python
>>> from hexpy import HexpySession, MetadataAPI
>>> session = HexpySession.load_auth_from_file()
>>> metadata_client = MetadataAPI(session)
>>> metadata_client.team_list()
>>> session.close()
```

## Methods

### team_list
```python
team_list() -> Dict[str, Any]
```
Return a list of teams accessible to the requesting user.

### monitor_list
```python
monitor_list(team_id: int) -> Dict[str, Any]
```
Returns a list of monitors accessible to the requesting or selected user along with metadata related to those monitors.

#### Arguments
* team_id: integer id number for a team

### geography
```python
geography() -> Dict[str, Any]
```
Return all the geographical locations that you may use to filter monitor results and to upload documents with location information.

### states
```python
states(country: str) -> Dict[str, Any]
```
Return all the states for a given country that you may use to filter monitor results and to upload documents with location information.

#### Arguments
* country: country code to filter states

### cities
```python
cities(country: str) -> Dict[str, Any]
```
Returns all the cities or urban areas defined in the given country that you may use to filter monitor results and to upload documents with location information. 

#### Arguments
* country: country: country code  to filter states

### countries
```python
countries() -> Dict[str, Any]
```
Returns all the countries that you may use to filter monitor results and to upload documents with location information.

### api_documentation
```python
api_documentation() -> Dict[str, Any]
```
Return latest JSON version of Crimson Hexagon API endpoint documentation.