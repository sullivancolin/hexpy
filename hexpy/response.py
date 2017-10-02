# -*- coding: utf-8 -*-
"""helper function for checking for valid responses."""


def handle_response(response, check_text=False):
    """Check that an API response is successful.

    Check response status code or response text
    Otherwise return data.

    # Arguments
        response: requests response object.
        check_text: Boolean (default= False).
    """
    if response.status_code != 200:
        raise ValueError("Bad request." + response.text)
    if check_text:
        if "error" in response.text:
            raise ValueError("Bad request." + response.text)
    return response.json()
