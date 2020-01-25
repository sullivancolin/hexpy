path: blob/master/src/hexpy
source: session.py

Session
=============

## Creating a session and generating a token for API requests.

<div class="termy">

```python
// Login using username and password
>>> from hexpy import HexpySession
>>> session = HexpySession.login(username="username@gmail.com", password="secretpassword")
// save token to ~/.hexpy/token.json
>>> session.save_token()

// or enter your password at the prompt
>>> session = HexpySession.login(username="username@email.com")
# Enter password: $ *********

// or instantiate a session using a saved token
>>> session = HexpySession(token="previously_saved_token")

// Create instance by loading token from file.  Default is `~/.hexpy/token.json`
>>> session = HexpySession.load_auth_from_file()
```
</div>

## Methods

### login
```python
login(username: str, password: str = None, no_expiration: bool = False, force: bool = False) -> HexpySession
```
Instantiate class from username and password.
#### Arguments
* username: account username.
* password: account password.
* no_expiration: True/False token with 24 expiration.

### save_token
```python
save_token(path: str = None) -> None
```
Save authorization token.
#### Arguments
* path: String, path to store API token. default is `~/.hexpy/token.json`

### load_auth_from_file
```python
load_auth_from_file(path: str = None) -> HexpySession
```
Instantiate class from previously saved token file.
#### Arguments
* path: String, path to store API token. default is default is `~/.hexpy/token.json`

### close

```python
close() -> None
```
Close open TCP connection to API server.

