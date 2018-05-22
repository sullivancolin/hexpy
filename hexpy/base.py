# -*- coding: utf-8 -*-
"""global variables for the API URL and rate limiting."""

import functools
from typing import Callable, Dict, Any, Union, Deque
import time
import threading
import collections
from requests.models import Response
import logging

logger = logging.getLogger(__name__)

ROOT = "https://api.crimsonhexagon.com/api/"

ONE_MINUTE = 60
MAX_CALLS = 120


def rate_limited(
    func: Callable, max_calls: int = MAX_CALLS, period: int = ONE_MINUTE
) -> Callable:
    """Limit the number of times a function can be called."""
    calls: Deque = collections.deque()

    # Add thread safety
    lock = threading.RLock()

    @functools.wraps(func)
    def wrapper(*args, **kargs):
        """Wrap function."""
        with lock:
            if len(calls) >= max_calls:
                until = time.time() + period - (calls[-1] - calls[0])
                sleeptime = until - time.time()
                if sleeptime > 0:
                    logger.info(
                        f"Rate Limit Reached. (Sleeping for {round(sleeptime)} seconds)"
                    )
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


def handle_response(response: Union[Response, Dict[str, Any]]) -> Dict[str, Any]:
    """Ensure responses do not contain errors, and Rate Limit is obeyed."""

    if not isinstance(response, dict):
        if response.status_code not in [200, 201, 202]:
            raise ValueError("Something Went Wrong. " + response.text)
        elif ("status" in response.json()) and response.json()["status"] == "error":
            raise ValueError("Something Went Wrong. " + response.text)
        return response.json()
    return response
