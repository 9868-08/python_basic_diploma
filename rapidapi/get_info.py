from json import JSONDecodeError
import requests
import json
from requests import Response, ConnectTimeout
from loader import bot
from states import bot_states
from requests import get, codes
import ast
import os
from config_data.config import RAPID_API_KEY


def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    # В зависимости от типа запроса вызываем соответствующую функцию
    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    else:
        return post_request(
            method_endswith,
            params
        )


def get_request(url, params):
    try:
        response = get(
            url,
            headers={
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            },
            params=params,
            timeout=15
        )
        if response.status_code == codes.ok:
            return response.json()
    except ConnectTimeout as error:  # Так как указали таймаут может быть прокинута ошибка - from requests.exceptions import ConnectTimeout
        print(error)  # Что-то делаем при возникновении ошибки


def post_request(method_endswith, payload):
    from config_data.config import RAPID_API_KEY
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", "https://hotels4.p.rapidapi.com/"+method_endswith, json=payload, headers=headers)
    #    print(response.text)
    if response.status_code == codes.ok:
        return response.json()
    return response.json()


def city_search(city_name):
    query_string = {'q': city_name, 'locale': 'ru_RU'}
    response = api_request(method_endswith='locations/v3/search',
                           params=query_string,
                           method_type='GET')

    return response
