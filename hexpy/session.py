"""Module for handling API authorization"""

import inspect
import json
import logging
from getpass import getpass

import requests
from pathlib import Path
from typing import Any, Dict

from .base import handle_response, rate_limited

logger = logging.getLogger(__name__)


class HexpySession:
    """Class for generating a token for use with all API requests.

    # Example Usage

    Login using username. Optionally include password, or enter it at the prompt.

    ```python
    >>> from hexpy import HexpySession
    >>> session = HexpySession.login(username="username@gmail.com", password="secretpassword")
    >>> session.save_token()
    ```
    or
    ```python
    >>> session = HexpySession.login(username="username@email.com")
    Enter password: *********
    >>> session.save_token()
    ```
    or instantiate a session using a saved token.
    ```python
    >>> session = HexpySession(token="previously_saved_token")
    ```
    Create instance by loading token from file.  Default is `~/.hexpy/token.json`
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

    TOKEN_FILE = Path.home() / ".hexpy" / "token.json"

    ROOT = "https://api.crimsonhexagon.com/api/"

    ONE_MINUTE = 60
    MAX_CALLS = 120

    def __init__(self, token: str) -> None:
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name == "get_token":
                setattr(self, name, rate_limited(fn, self.MAX_CALLS, self.ONE_MINUTE))

        self.auth = {"auth": token}
        self.session = requests.Session()
        self.session.params = self.auth

    @classmethod
    def _get_token(
        cls,
        username: str,
        password: str,
        no_expiration: bool = False,
        force: bool = False,
    ) -> Dict[str, Any]:
        """Request authorization token.

        # Arguments
            username: String, account username.
            password: String, account password.
            no_expiration: Boolean, if True, token does not expire in 24 hours.
            force: Boolean, if true, forces authentication token update for the requesting user.
        """
        return handle_response(
            requests.Session().get(
                cls.ROOT + "authenticate",
                params={
                    "username": username,
                    "password": password,
                    "noExpiration": str(no_expiration).lower(),
                    "force": str(force).lower(),
                },
            )
        )

    def save_token(self, path: str = None) -> None:
        """Save authorization token.

        # Arguments
            path: String, path to store token. default is `~/.hexpy/token.json`
        """
        if not path:
            token_path = self.TOKEN_FILE
        else:
            token_path = Path(path)
        if not token_path.exists():
            parent = token_path.parent
            if not parent.exists():
                token_path.parent.mkdir()
        with open(token_path, "w") as outfile:
            json.dump(self.auth, outfile, indent=4)

    @classmethod
    def login(
        cls,
        username: str,
        password: str = None,
        no_expiration: bool = False,
        force: bool = False,
    ):
        """
        Instantiate class from username and password.

        # Arguments
            username: String, account username.
            password: String, account password.
            no_expiration: Boolean, if True, token does not expire in 24 hours.
            force: Boolean, if true, forces authentication token update for the requesting user.
        """
        if password is None:
            password = getpass(prompt="Enter password: ")

        auth = cls._get_token(username, password, no_expiration, force)
        return cls(auth["auth"])

    @classmethod
    def load_auth_from_file(cls, path: str = None):
        """Instantiate class from previously saved token file.

        # Arguments
            path: String, path to store API token. default is default is `~/.hexpy/token.json`
        """
        try:
            if not path:
                cred_path = cls.TOKEN_FILE
            else:
                cred_path = Path(path)
            with open(cred_path) as infile:
                auth = json.load(infile)
                logger.info(f"using token: {json.dumps(auth)}")
                return cls(token=auth["auth"])
        except IOError:
            raise IOError(
                f"Credentials File at '{cred_path}' not found. Please specify token or username and password."
            )

    def close(self):
        """Close persisted connection to API server."""
        self.session.close()

    def __enter__(self):
        """Use HexpySession with Context Manager."""
        return self

    def __exit__(self, *args):
        """Exit Context Manager and close session."""
        self.close()
