path: blob/master/src/hexpy
source: custom.py


Custom API
===========

Class for creating a custom API

## Example usage
<div class="termy">

```python
>>> from hexpy import HexpySession , CustomAPI
>>> session = HexpySession.load_auth_from_file()
>>> custom_client = CustomAPI(session, "/some/endpoint/")
>>> custom_client.get(url_params="<url_param1>/path", params={"query_string_param":some_value})
```
</div>

## Methods

### get
```python
get(url_params: str = "", params: Dict[str, Any] = None) -> JSONDict
```
Send get request using URL parameters and query-string parameters.

#### Arguments:
* url_params: String, url params and endpoints concatenated.
* params: Dict, querystring params.

### post
```python
post(url_params: str = "", params: Dict[str, Any] = None, data: Dict[str, Any] = None, ) -> JSONDict
```
Send post request using URL parameters and query-string parameters, and json data.

#### Arguments
* url_params: String, url params and endpoints concatenated.
* params: Dict, querystring params.
* data: Dict, json data to post.

### delete
```python
delete(url_params: str = "", params: Dict[str, Any] = None) -> JSONDict
```
Send delete request using URL parameters and query-string parameters.

#### Arguments
* url_params: String, url params and endpoints concatenated.
* params: Dict, querystring params.