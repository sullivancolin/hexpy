"""rate limiting decorator and handling responses for exceptions and JSON conversion"""

import functools
import logging
import threading
import time
from collections import deque

from requests.models import Response
from typing import Any, Callable, Deque, Dict, Union


def rate_limited(func: Callable, max_calls: int, period: int) -> Callable:
    """Limit the number of times a function can be called."""
    calls: Deque = deque()

    # Add thread safety
    lock = threading.RLock()
    logger = logging.getLogger(func.__name__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Wrap function."""
        with lock:
            if len(calls) >= max_calls:
                until = time.time() + period - (calls[-1] - calls[0])
                sleeptime = until - time.time()
                if sleeptime > 0:
                    logger.info(
                        f"Rate Limit Reached. (Sleeping for {round(sleeptime + 10)} seconds)"
                    )
                    time.sleep(sleeptime + 10)
                while len(calls) > 0:
                    calls.popleft()
            calls.append(time.time())

            # Pop the timestamp list front (ie: the older calls) until the sum goes
            # back below the period. This is our 'sliding period' window.
            while (calls[-1] - calls[0]) >= period:
                calls.popleft()

        return func(*args, **kwargs)

    return wrapper


def handle_response(response: Union[Response, Dict[str, Any]]) -> Dict[str, Any]:
    """Ensure responses do not contain errors."""

    if isinstance(response, Response):
        if not response.ok:
            raise ValueError("Something Went Wrong. " + response.text)
        elif ("status" in response.json()) and response.json()["status"] == "error":
            raise ValueError("Something Went Wrong. " + response.text)
        return response.json()
    else:
        return response
