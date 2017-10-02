# Authorization

## Generating a token for use with all API requests.

Instantiate using account token, or username. Optionally include password, or enter it at the prompt.

```python
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

`get_token(self, username, password, no_expiration=True)`

Request authorization token.
#### Arguments

* username: account username.
* password: account password.
* no_expiration: True/False token with 24 expiration.

### save_token
`save_token(self, path=None)`

Save authorization token.
#### Arguments
* path: String, path to store credentials. default is `~/.hexpy/credentials.json`

### load_auth_from_file()
`load_auth_from_file(self, path=None)`

Instantiate class from previously saved credentials file.
#### Arguments
* path: String, path to store credentials. default is `~/.hexpy/credentials.json`
