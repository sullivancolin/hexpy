# -*- coding: utf-8 -*-
"""global variables for the API URL and rate limiting."""

import functools
from typing import Callable
import time
import threading
import collections

ROOT = "https://api.crimsonhexagon.com/api/"

ONE_MINUTE = 60
MAX_CALLS = 120


def rate_limited(max_calls, period=1.0):
    def decorator(func):
        calls = collections.deque()

        # Add thread safety
        lock = threading.RLock()

        @functools.wraps(func)
        def wrapper(*args, **kargs):
            '''Decorator wrapper function'''
            with lock:
                if len(calls) >= max_calls:
                    until = time.time() + period - (calls[-1] - calls[0])
                    sleeptime = until - time.time()
                    if sleeptime > 0:
                        print("Rate Limit Reached. (Sleeping for {} seconds)".
                              format(round(sleeptime)))
                        time.sleep(sleeptime)
                    while len(calls) > 0:
                        calls.popleft()
                calls.append(time.time())

                # Pop the timestamp list front (ie: the older calls) until the sum goes
                # back below the period. This is our 'sliding period' window.
                while (calls[-1] - calls[0]) >= period:
                    calls.popleft()

            return func(*args, **kargs)

        return wrapper

    return decorator


def response_handler(f: Callable) -> Callable:
    """Ensure responses do not contain errors, and Rate Limit is obeyed."""

    @rate_limited(max_calls=MAX_CALLS, period=ONE_MINUTE)
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        if not isinstance(response, dict):
            if response.status_code not in [200, 201, 202]:
                raise ValueError("Something Went Wrong. " + response.text)
            elif ("status" in response.json()
                  ) and response.json()["status"] == "error":
                raise ValueError("Something Went Wrong. " + response.text)
            return response.json()
        return response

    return wrapped
