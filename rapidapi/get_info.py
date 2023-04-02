#import requests
import json
from requests import get, codes


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
            url=url,
            params=params
        )


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
            return response.json()
    except BaseException:
        ...


def post_request(url, params):
    headers = {
        "content-type": "application/json",
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
            return response.json()
    except BaseException:
        ...


def def_get_location_id(city: str):
    import requests
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    #    querystring = {"q": "new york", "locale": "ru_RU"}
    querystring = {"q": city, "locale": "ru_RU"}

    headers = {
        "X-RapidAPI-Key": "7d70182871msh0110c820c62cce9p13613fjsna334f8c7dfe3",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


#    print(response.text)


def def_hotel_id(location_id: int):
    import requests

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": location_id},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 150,
            "min": 100
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "7d70182871msh0110c820c62cce9p13613fjsna334f8c7dfe3",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    #    print(response.text)
    return response.json()


def def_hotel_detail(hotel_id: int):
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "f11fe670bamshdaffc29f3f33e2bp19bde9jsn5f0726b4228a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)

    # this line converts the response to a python dict which can then be parsed easily
    response_dict = json.loads(response.text)

    #    print(response_dict['data']['propertyInfo'])
    return response_dict


def def_rapidapy_start(city):
    city = "Boston"
    location_json = def_get_location_id(city)
    location_id = location_json['sr'][0]['gaiaId']
    #    print(city, "id=", location_id)
    hotel_id_json = def_hotel_id(location_id)
    #  hotel_id_json['data']['propertySearch']['properties'][0]['id']:
    parsed = hotel_id_json['data']['propertySearch']
    hotel_id_list = []
    for item in parsed['properties']:
        hotel_id_list.append(item['id'])
    return hotel_id_list
