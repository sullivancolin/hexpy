# -*- coding: utf-8 -*-
"""Module for handling API authorization"""

import requests
import os
import json
from getpass import getpass
from ratelimiter import RateLimiter
from .response import handle_response
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class CrimsonAuthorization(object):
    """Generating a token for use with all API requests.

    Instantiate with token, or username. Optionally include password, or enter it at the prompt.

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
    """

    CREDS_FILE = os.path.join(
        os.path.expanduser('~'), '.hexpy', 'credentials.json')

    def __init__(self, username=None, password=None, token=None):
        super(CrimsonAuthorization, self).__init__()
        if not any([username, password, token]):
            raise ValueError(
                "No credentials given. Please provide valid token or username and password")
        else:
            if not token:

                if username and not password:
                    password = getpass(prompt='Enter password: ')
                elif password and not username:
                    raise ValueError("Missing username.")

                self.auth = self.get_token(username, password)
                self.token = self.auth["auth"]
            else:
                # TODO Test of validity of provided token
                self.token = token

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def get_token(self, username, password, no_expiration=True):
        """Request authorization token.
        # Arguments
            username: account username.
            password: account password.
            no_expiration: True/False token with 24 expiration.
        """
        response = handle_response(
            requests.get(
                ROOT +
                "authenticate?username={username}&password={password}&noExpiration={expiration}".format(
                    username=username,
                    password=password,
                    expiration=str(no_expiration).lower())))
        return response

    def save_token(self, path=None):
        """Request authorization token.
        # Arguments
            path: path to store credentials. default is
        """
        if not path:
            path = self.CREDS_FILE
        if not os.path.exists(os.path.split(path)[0]):
            os.makedirs(os.path.split(path)[0])
        with open(path, "w") as outfile:
            json.dump({"auth": self.token}, outfile, indent=4)

    @classmethod
    def load_auth_from_file(cls, path=None):
        """Instanciate class from previously saved credentials file.
        # Arguments
            path: path to store credentials. default is
        """
        try:
            if not path:
                path = cls.CREDS_FILE
            with open(path) as infile:
                auth = json.load(infile)
                return cls(token=auth["auth"])
        except FileNotFoundError:
            raise FileNotFoundError(
                "Credentials File not found. Please specify token or username and password.")
