# -*- coding: cp1251 -*-

from requests import get, codes


def api_request(method_endswith,
                # locations/v3/search ���� properties/v2/list
                params,
                # params,  # ���������, ���� locations/v3/search, �� {'q': '����', 'locale': 'ru_RU'}
                method_type
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    # � ����������� �� ���� ������� �������� ��������������� �������
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
    try:
        response = get(
            url,
            headers=...,
            params=params,
            timeout=15
        )
        if response.status_code == codes.ok:
            return response.json()
    except None:
        print("exception")


api_request('method_endswith', 'params', 'GET')