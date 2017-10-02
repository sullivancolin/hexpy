# -*- coding: utf-8 -*-
"""global variables for the API URL and rate limiting."""

ROOT = "https://api.crimsonhexagon.com/api/"

ONE_MINUTE = 60
MAX_CALLS = 120


def sleep_message(until):
    """Output message when rate limit reached.

    # Arguments
        until: time in milliseconds until able to call API again.
    """
    pass
    # print('Rate limit reached, sleeping for {minute} seconds.'.format(
    #     minute=ONE_MINUTE))
