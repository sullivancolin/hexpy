Custom API
===========

## Class for creating a custom API

## Example usage.

```python
>>> from hexpy import HexpySession , CustomAPI
>>> session = HexpySession.load_auth_from_file()
>>> custom_client = CustomAPI(session, "/some/endpoint/")
>>> custom_client.get(url_params="<url_param1>/path", params={"query_string_param":some_value})
```

## Methods

### get
```python
get(url_params: str = "", params: Dict[str, Any] = None) -> Dict[str, Any]
```
Send get request using URL parameters and query-string parameters.

#### Arguments:
* url_params: String, url params and endpoints concatenated.
* params: Dict, querystring params.

### post
```python
post(url_params: str = "", params: Dict[str, Any] = None, data: Dict[str, Any] = None, ) -> Dict[str, Any]
```
Send post request using URL parameters and query-string parameters, and json data.

#### Arguments
* url_params: String, url params and endpoints concatenated.
* params: Dict, querystring params.
* data: Dict, json data to post.

### delete
```python
delete(url_params: str = "", params: Dict[str, Any] = None) -> Dict[str, Any]
```
Send delete request using URL parameters and query-string parameters.

#### Arguments
* url_params: String, url params and endpoints concatenated.
* params: Dict, querystring params.