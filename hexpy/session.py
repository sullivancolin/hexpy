# -*- coding: utf-8 -*-
"""Module for handling API authorization"""

import inspect
import requests
from requests.models import Response
from pathlib import Path
import json
from getpass import getpass
from .base import ROOT, response_handler


class HexpySession(object):
    """Class for generating a token for use with all API requests.

    # Example Usage

    Instantiate with token, or username. Optionally include password, or enter it at the prompt.

    ```python
    >>> from hexpy import HexpySession
    >>> session = HexpySession(username="username@gmail.com", password="secretpassword")
    >>> session.save_token()
    ```
    or
    ```python
    >>> session = HexpySession(username="username@email.com")
    Enter password: *********
    >>> session.save_token()
    ```
    or
    ```python
    >>> session = HexpySession(token="previously_saved_token")
    ```
    Create instance by loading token from file.  Default is `~/.hexpy/credentials.json`
    ```python
    >>> session = HexpySession.load_auth_from_file()
    ```

    Create instance with context manager to close TCP session automatically when finished
    ```python
    >>> with HexpySession.load_auth_from_file() as session:
    ...:     client = MonitorAPI(session)
    ...:     # use client to call API multiple times with same session

    >>> # session TCP connection is closed until next call to API
    ```
    """

    CREDS_FILE = Path.home() / '.hexpy' / 'credentials.json'

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 token: str = None,
                 no_expiration: bool = False) -> None:
        super(HexpySession, self).__init__()
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name == "get_token":
                setattr(self, name, response_handler(fn))
        if not any([username, password, token]):
            raise ValueError(
                "No credentials given. Please provide valid token or username and password"
            )
        else:
            if not token:
                if username and not password:
                    password = getpass(prompt='Enter password: ')
                elif password and not username:
                    raise ValueError("Missing username.")
                self.auth = self.get_token(username, password, no_expiration)
                self.session = requests.Session()
                self.session.params = {"auth": self.auth["auth"]}
            else:
                # TODO Test of validity of provided token
                self.auth = {"auth": token}
                self.session = requests.Session()
                self.session.params = self.auth

    def get_token(self,
                  username: str,
                  password: str,
                  no_expiration: bool = False) -> Response:
        """Request authorization token.

        # Arguments
            username: String, account username.
            password: String, account password.
            no_expiration: Boolean, if True, token does not expire in 24 hours.
        """
        return requests.Session().get(
            ROOT + "authenticate",
            params={
                "username": username,
                "password": password,
                "noExpiration": no_expiration,
            })

    def save_token(self, path: str = None) -> None:
        """Save authorization token.

        # Arguments
            path: String, path to store credentials. default is `~/.hexpy/credentials.json`
        """
        if not path:
            path = self.CREDS_FILE
            if not path.exists():
                path.parent.mkdir()
        with open(path, "w") as outfile:
            json.dump(self.auth, outfile, indent=4)

    @classmethod
    def load_auth_from_file(cls, path: str = None):
        """Instantiate class from previously saved credentials file.

        # Arguments
            path: path to store credentials. default is default is `~/.hexpy/credentials.json`
        """
        try:
            if not path:
                path = cls.CREDS_FILE
            with open(path) as infile:
                auth = json.load(infile)
                return cls(token=auth["auth"])
        except IOError:
            raise IOError(
                "Credentials File at '{}' not found. Please specify token or username and password.".
                format(path))

    def close(self):
        """Close persisted connection to API server."""
        self.session.close()

    def __enter__(self):
        """Use HexpySession with Context Manager."""
        return self

    def __exit__(self, *args):
        """Exit Context Manager and close session."""
        self.close()