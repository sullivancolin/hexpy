def handle_response(response, check_text=False):
    if response.status_code != 200:
        raise ValueError("Bad request." + response.text)
    if check_text:
        if "error" in response.text:
            ValueError("Bad request." + response.text)
    return response.json()
