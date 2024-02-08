from rapidapi.get_info import api_request


# формируем локации по указанному городу
def city_search(city_name):
    query_string = {'q': city_name, 'locale': 'en_US'}
    response = api_request(method_endswith='locations/v3/search',
                           params=query_string,
                           method_type='GET')
    if response:
        cities = list()
        for i in response['sr']:
            if i['type'] == "CITY":
                cities.append(
                    dict(id=i['gaiaId'],
                         region_name=i['regionNames']['fullName'])
                )
        return cities
