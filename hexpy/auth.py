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
    """Client class for interacting with Crimson Hexagon API"""
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
        response = handle_response(
            requests.get(
                ROOT +
                "authenticate?username={username}&password={password}&noExpiration={expiration}".format(
                    username=username,
                    password=password,
                    expiration=str(no_expiration).lower())))
        return response

    def save_token(self):
        if not os.path.exists(os.path.split(self.CREDS_FILE)[0]):
            os.makedirs(os.path.split(self.CREDS_FILE)[0])
        with open(self.CREDS_FILE, "w") as outfile:
            json.dump({"auth": self.token}, outfile, indent=4)

    @classmethod
    def load_auth_from_cache(cls, path=None):

        try:
            if not path:
                with open(cls.CREDS_FILE) as infile:
                    auth = json.load(infile)
                    return cls(token=auth["auth"])
            else:
                with open(path) as infile:
                    auth = json.load(infile)
                    return cls(token=auth["auth"])
        except FileNotFoundError:
            raise FileNotFoundError(
                "Credentials File not found. Please specify token or username and password.")
