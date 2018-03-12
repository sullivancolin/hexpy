# -*- coding: utf-8 -*-
"""Module for handling API authorization"""

import inspect
import requests
from pathlib import Path
import json
from getpass import getpass
from .base import ROOT, handle_response, rate_limited
from typing import Dict, Any


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

    CRED_FILE = Path.home() / '.hexpy' / 'credentials.json'

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 token: str = None,
                 no_expiration: bool = False) -> None:
        super(HexpySession, self).__init__()
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name == "get_token":
                setattr(self, name, rate_limited(fn))
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
                  no_expiration: bool = False) -> Dict[str, Any]:
        """Request authorization token.

        # Arguments
            username: String, account username.
            password: String, account password.
            no_expiration: Boolean, if True, token does not expire in 24 hours.
        """
        return handle_response(requests.Session().get(
            ROOT + "authenticate",
            params={
                "username": username,
                "password": password,
                "noExpiration": str(no_expiration).lower(),
            }))

    def save_token(self, path: str = None) -> None:
        """Save authorization token.

        # Arguments
            path: String, path to store credentials. default is `~/.hexpy/credentials.json`
        """
        if not path:
            cred_path = self.CRED_FILE
        else:
            cred_path = Path(path)
        if not cred_path.exists():
            parent = cred_path.parent
            if not parent.exists():
                cred_path.parent.mkdir()
        with open(cred_path, "w") as outfile:
            json.dump(self.auth, outfile, indent=4)

    @classmethod
    def load_auth_from_file(cls, path: str = None):
        """Instantiate class from previously saved credentials file.

        # Arguments
            path: path to store credentials. default is default is `~/.hexpy/credentials.json`
        """
        try:
            if not path:
                cred_path = cls.CRED_FILE
            else:
                cred_path = Path(path)
            with open(cred_path) as infile:
                auth = json.load(infile)
                return cls(token=auth["auth"])
        except IOError:
            raise IOError(
                "Credentials File at '{}' not found. Please specify token or username and password.".
                format(cred_path))

    def close(self):
        """Close persisted connection to API server."""
        self.session.close()

    def __enter__(self):
        """Use HexpySession with Context Manager."""
        return self

    def __exit__(self, *args):
        """Exit Context Manager and close session."""
        self.close()