my_dict = {'@type': 'gaiaRegionResult', 'index': '0', 'gaiaId': '660', 'type': 'CITY',
           'regionNames': {'fullName': 'Бостон, Suffolk County, Массачусетс, США', 'shortName': 'Бостон',
                           'displayName': 'Бостон, Suffolk County, Массачусетс, США', 'primaryDisplayName': 'Бостон',
                           'secondaryDisplayName': 'Suffolk County, Массачусетс, США', 'lastSearchName': 'Бостон'},
           'essId': {'sourceName': 'GAI', 'sourceId': '660'}, 'coordinates': {'lat': '42.35936', 'long': '-71.05979'},
           'hierarchyInfo': {'country': {'name': 'Соединенные Штаты', 'isoCode2': 'US', 'isoCode3': 'USA'}}}
result = list()
result.append(
    dict(id=my_dict['gaiaId'],
         region_name=my_dict['regionNames']['fullName']))

print(result)
