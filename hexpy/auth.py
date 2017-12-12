# -*- coding: utf-8 -*-
"""Module for handling API authorization"""

import requests
import os
import json
from getpass import getpass
from .base import ROOT, response_handler


class HexpyAuthorization(object):
    """Class for generating a token for use with all API requests.

    # Example Usage

    Instantiate with token, or username. Optionally include password, or enter it at the prompt.

    ```python
    >>> from hexpy import HexpyAuthorization
    >>> auth = HexpyAuthorization(username="username@gmail.com", password="secretpassword")
    >>> auth.save_token()
    ```
    or
    ```python
    >>> auth = HexpyAuthorization(username="username@email.com")
    Enter password: *********
    >>> auth.save_token()
    ```
    or
    ```python
    >>> auth = HexpyAuthorization(token="previously_saved_token")
    ```
    Create instance by loading token from file.  Default is `~/.hexpy/credentials.json`
    ```python
    >>> auth = HexpyAuthorization.load_auth_from_file()
    ```

    Create instance with context manager to close TCP session automatically when finished
    ```python
    >>> with HexpyAuthorization.load_auth_from_file() as auth:
    ...:     client = MonitorAPI(auth)
    ...:     # use client to call API multiple times with same session

    >>> # auth TCP session is closed until next call to API
    ```

    """

    CREDS_FILE = os.path.join(
        os.path.expanduser('~'), '.hexpy', 'credentials.json')

    def __init__(self,
                 username=None,
                 password=None,
                 token=None,
                 no_expiration=False):
        super(HexpyAuthorization, self).__init__()
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
                self.token = self.auth["auth"]
                self.session = requests.Session()
                self.session.params = {"auth": self.token}
            else:
                # TODO Test of validity of provided token
                self.token = token
                self.session = requests.Session()
                self.session.params = {"auth": self.token}

    @response_handler
    def get_token(self, username, password, no_expiration=False):
        """Request authorization token.

        # Arguments
            username: String, account username.
            password: String, account password.
            no_expiration: Boolean, if True, token does not expire in 24 hours.
        """
        return requests.get(
            ROOT + "authenticate",
            params={
                "username": username,
                "password": password,
                "noExpiration": no_expiration,
            })

    def save_token(self, path=None):
        """Save authorization token.

        # Arguments
            path: String, path to store credentials. default is `~/.hexpy/credentials.json`
        """
        if not path:
            path = self.CREDS_FILE
        if not os.path.exists(os.path.split(path)[0]):
            os.makedirs(os.path.split(path)[0])
        with open(path, "w") as outfile:
            json.dump({"auth": self.token}, outfile, indent=4)

    @classmethod
    def load_auth_from_file(cls, path=None):
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
                "Credentials File not found. Please specify token or username and password."
            )

    def close(self):
        """Close persisted connection to API server."""
        self.session.close()
        return self

    def __enter__(self):
        """Use HexpyAuthorization with Context Manager."""
        return self

    def __exit__(self, *args):
        """Exit Context Manager and close session."""
        self.close()