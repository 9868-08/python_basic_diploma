import requests
from config_data.config import RAPID_API_KEY


# Функция, которая делает запросы к API
def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'en_US'}
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


# get запросы к API
def get_request(url, params):
    try:
        response = requests.get(
            url,
            headers={
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            },
            params=params,
            timeout=15
        )
        print("Status Code", response.json())
        if response.status_code == 200:
            return response.json()
    except ConnectionError as error:  # Так как указали таймаут может быть прокинута ошибка -
        # from requests.exceptions import ConnectTimeout
        print(error)  # Что-то делаем при возникновении ошибки


# post запросы к API
def post_request(method_endswith, payload):
    from config_data.config import RAPID_API_KEY
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", "https://hotels4.p.rapidapi.com/"+method_endswith,
                                json=payload, headers=headers)
    #    print(response.text)
    if response.status_code == 200:
        return response.json()
    return response.json()