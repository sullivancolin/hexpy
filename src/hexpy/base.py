"""rate limiting decorator and handling responses for exceptions and JSON conversion"""

import functools
import logging
import threading
import time
from collections import deque
from typing import Any, Callable, Deque, Dict

from requests.models import Response

JSONDict = Dict[str, Any]


def rate_limited(
    func: Callable[..., JSONDict], max_calls: int, period: int
) -> Callable[..., JSONDict]:
    """Limit the number of times a function can be called."""
    calls: Deque = deque()

    # Add thread safety
    lock = threading.RLock()
    logger = logging.getLogger(func.__name__)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> JSONDict:
        """Wrap function."""
        with lock:
            if len(calls) >= max_calls:
                until = time.time() + period - (calls[-1] - calls[0])
                sleeptime = until - time.time()
                if sleeptime > 0:
                    logger.info(
                        f"Rate Limit Reached. (Sleeping for {round(sleeptime + 5)} seconds)"
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


def handle_response(response: Response) -> JSONDict:
    """Ensure responses do not contain errors."""

    if not response.ok:
        raise ValueError(f"Something Went Wrong. {response.text}")
    elif ("status" in response.json()) and response.json()["status"] == "error":
        raise ValueError(f"Something Went Wrong. {response.text}")
    return response.json()
