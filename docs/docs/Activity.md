# Activity API

## Class for working with Crimson Hexagon Activity Report API.

## Example Usage

```python
>>> from hexpy import HexpySession, ActivityAPI
>>> session = HexpySession.load_auth_from_file()
>>> activity_client = ActivityAPI(session)
>>> activity_client.monitor_creation(organization_id)
>>> session.close()
```

## Methods

### monitor_creation
```python
monitor_creation(organization_id: int) -> Dict[str, Any]
```
Get Monitor Creation Report for all teams within an organization and how many monitors were created during a given time period.


#### Arguments
* organiztion_id: Integer, the id of the organization being requested.

### social_sites
```python
social_sites(organization_id: int) -> Dict[str, Any]
```
Get Social Site Report and associated usernames for Teams within an Organization.

#### Arguments
* organiztion_id: Integer, the id of the organization being requested.

### user_activity
```python
user_activity(organization_id: int) -> Dict[str, Any]
```
Get a list of users indicating when they last logged into the platform, the last monitor they created, and the last monitor they viewed.

#### Arguments
* organiztion_id: Integer, the id of the organization being requested.

### user_invitations
```python
user_invitations(organization_id: int) -> Dict[str, Any]
```
Get a list of users within an Organization and which Team(s) they were invited to.

#### Arguments
* organiztion_id: Integer, the id of the organization being requested.
