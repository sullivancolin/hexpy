Authorization
=============

## Generating a token for use with all API requests.

Instantiate using token, or username. Optionally include password, or enter it at the prompt.
```python
>>> from hexpy import CrimsonAuthorization
>>> auth = CrimsonAuthorization(username="username@gmail.com", password="secretpassword")
>>> auth.save_token()
```
or
```python
>>> auth = CrimsonAuthorization(username="username@email.com")
Enter password: *********
>>> auth.save_token()
```
or
```python
>>> auth = CrimsonAuthorization(token="previously_saved_token")
```
Create instance by loading token from file.  Default is `~/.hexpy/credentials.json`
```python
>>> auth = CrimsonAuthorization.load_auth_from_file()
```

## Methods

### get_token

```python
get_token(username, password, no_expiration=False)
```

Request authorization token.
#### Arguments

* username: account username.
* password: account password.
* no_expiration: True/False token with 24 expiration.

### save_token
```python
save_token(path=None)
```
Save authorization token.
#### Arguments
* path: String, path to store credentials. default is `~/.hexpy/credentials.json`

### load_auth_from_file
```python
load_auth_from_file(path=None)
```
Instantiate class from previously saved credentials file.
#### Arguments
* path: String, path to store credentials. default is `~/.hexpy/credentials.json`
