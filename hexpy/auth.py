# -*- coding: utf-8 -*-
"""Main module."""
import requests
import os
import json
from response import handle_response

ONE_MINUTE = 60
ROOT = "https://api.crimsonhexagon.com/api/"


class CrimsonAuthorization(object):
    """Client class for interacting with Crimson Hexagon API"""

    CREDS_FILE = os.path.join(
        os.path.expanduser('~'), '.hexpy', 'credentials.json')

    def __init__(self, username=None, password=None, token=None):
        super(CrimsonAuthorization, self).__init__()
        if not any([username, password, token]):
            self.load_auth_from_cache()
        else:
            if not token:
                if not (username and password):
                    raise ValueError("Missing user name or password.")
                else:
                    self.get_token(username, password)
            else:
                self.token = token

    def get_token(self, username, password, no_expiration=True):
        response = handle_response(
            requests.get(
                ROOT +
                "authenticate?username={username}&password={password}&noExpiration={expiration}".format(
                    username=username,
                    password=password,
                    expiration=str(no_expiration).lower())))
        self.token = response["auth"]

    def save_token(self):
        if not os.path.exists(os.path.split(self.CREDS_FILE)[0]):
            os.makedirs(os.path.split(self.CREDS_FILE)[0])
        with open(self.CREDS_FILE, "w") as outfile:
            json.dump({"auth": self.token}, outfile, indent=4)

    def load_auth_from_cache(self):
        try:
            with open(self.CREDS_FILE) as infile:
                auth = json.load(infile)
                self.token = auth["auth"]
        except FileNotFoundError as e:
            raise e(
                "{} not found. Please specify token or username and password.".format(
                    self.CREDS_FILE))


if __name__ == '__main__':

    client = CrimsonAuthorization()

    client.save_token()

    client = CrimsonAuthorization()