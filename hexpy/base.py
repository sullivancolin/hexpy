# -*- coding: utf-8 -*-
"""global variables for the API URL and rate limiting."""
import functools
from halo import Halo
from ratelimiter import RateLimiter
import time
import threading

ROOT = "https://api.crimsonhexagon.com/api/"

ONE_MINUTE = 60
MAX_CALLS = 120


class SpinnerLimiter(RateLimiter):
    """Rate limiting with spinner information."""

    def __enter__(self):
        """When limiter sleeps, show spinner with wait time."""
        with self._lock:
            # We want to ensure that no more than max_calls were run in the allowed
            # period. For this, we store the last timestamps of each call and run
            # the rate verification upon each __enter__ call.
            if len(self.calls) >= self.max_calls:
                until = time.time() + self.period - self._timespan
                if self.callback:
                    t = threading.Thread(target=self.callback, args=(until, ))
                    t.daemon = True
                    t.start()
                sleeptime = until - time.time()
                with Halo(text="Rate Limit Reached. (Sleeping for {} seconds)".
                          format(round(sleeptime))):
                    if sleeptime > 0:
                        time.sleep(sleeptime)
            return self


def response_handler(f):
    """Ensure responses do not contain errors, and Rate Limit is obeyed."""

    @SpinnerLimiter(max_calls=MAX_CALLS, period=ONE_MINUTE)
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code not in [200, 201, 202]:
            raise ValueError("Something Went Wrong." + response.text)
        elif ("status" in response.json()
              ) and response.json()["status"] == "error":
            raise ValueError("Something Went Wrong. " + response.text)
        return response.json()

    return wrapped
