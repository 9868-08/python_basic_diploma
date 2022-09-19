import os

"""
This script is used to change the RapidApi key if the key request limit has been reached.
"""


def get_correct_rapidapi_key():
    is_requests_amount_are_over = os.getenv('REQUESTS_LIMIT_REACHED')

    if is_requests_amount_are_over == 'False':
        return os.getenv('RAPID_API_KEY')
    elif is_requests_amount_are_over == 'True':
        return os.getenv('ANOTHER_RAPID_API_KEY')


def change_rapid_api_key():
    is_requests_amount_are_over = os.getenv('REQUESTS_LIMIT_REACHED')

    if is_requests_amount_are_over == 'False':
        os.environ['REQUESTS_LIMIT_REACHED'] = 'True'
    elif is_requests_amount_are_over == 'True':
        os.environ['REQUESTS_LIMIT_REACHED'] = 'False'


def get_headers_by_correct_rapidapi_key() -> dict:
    rapid_api_key = get_correct_rapidapi_key()
    return {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
