Metadata API
============

## Class for working with Crimson Hexagon account and analysis metadata.

## Example usage.

```python
>>> from hexpy import HexpyAuthorization, MetadataAPI
>>> auth = HexpyAuthorization.load_auth_from_file()
>>> metadata_client = MetadataAPI(auth)
>>> metadata_client.team_list()
```

## Methods

### team_list
```python
analysis_request(data)
```
Return a list of teams accessible to the requesting user.

### monitor_list
```python
monitor_list(team_id)
```
Returns a list of monitors accessible to the requesting or selected user along with metadata related to those monitors.

#### Arguments
* team_id: integer id number for a team

### geography
```python
geography()
```
Return all the geographical locations that you may use to filter monitor results and to upload documents with location information.

### states
```python
states(country)
```
Return all the states for a given country that you may use to filter monitor results and to upload documents with location information.

#### Arguments
* country: country code to filter states

### cities
```python
cities(country)
```
Returns all the cities or urban areas defined in the given country that you may use to filter monitor results and to upload documents with location information. 

#### Arguments
* country: country: country code  to filter states

### countries
```python
countries()
```
Returns all the countries that you may use to filter monitor results and to upload documents with location information.
