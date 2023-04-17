from json import JSONDecodeError
import requests
import json
from requests import Response
from loader import bot
from states import bot_states
from requests import get, codes
import ast


def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    # В зависимости от типа запроса вызываем соответствующую функцию
    if method_type == 'GET':
        return get_request(
            url,
            params
        )
    else:
        return post_request(url, params)


def get_request(url, params):
    headers = {
        "X-RapidAPI-Key": "7d70182871msh0110c820c62cce9p13613fjsna334f8c7dfe3",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    try:
        response = get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )
        if response.status_code == codes.ok:
            # return response.json()
            cities = list()
            # cities_dict = dict()
            response_text = response.text
            response_dict = ast.literal_eval(response_text)
            for i in response_dict['sr']:
                # Возможно ключи стоит поправить - проверьте работоспособность
                cities.append(
                    dict(id=i['gaiaId'],
                         region_name=i['regionNames']['fullName'])
                )
            return cities

    except Exception as e:
        print(e)
        #    except BaseException:
        ...


def post_request(method_endswith, params):
    payload = params

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "7d70182871msh0110c820c62cce9p13613fjsna334f8c7dfe3",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", method_endswith, json=payload, headers=headers)
    #    print(response.text)
    if response.status_code == codes.ok:
        return response.json()
    return response.json()
