from rapidapi.get_info import api_request
from loader import bot


def bot_payload(message):
    bot_sort = ""
    with bot.retrieve_data(message.from_user.id) as data:
        print(data['check_in'])
        print(data['check_out'])
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": "6054439"},
        "checkInDate": {    # replace with values print(data['check_in'])
            "day": 10,
            "month": 10,
            "year": 2024
        },
        "checkOutDate": {    # replace with values print(data['check_out'])
            "day": 15,
            "month": 10,
            "year": 2024
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": bot_sort,
        "filters": {"price": {
            "max": 150,
            "min": 100
        }}
    }
    hotel_id_json = api_request('properties/v2/list', payload, 'POST')
    parsed_dict = hotel_id_json['data']['propertySearch']
    # hotel_id_list = []
    founded_hotel = []
    count = 1
    for item in parsed_dict['properties']:
        if count > int(data['how_much_hotels']):
            break
            data['distanceFromDestination'] = item['destinationInfo']['distanceFromDestination']['value']
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": item['id']
        }
        properties_v2_detail_responce = api_request('properties/v2/detail', payload, 'POST')
        data['address'] = (
            properties_v2_detail_responce)['data']['propertyInfo']['summary']['location']['address']['addressLine']
        data['price'] = item['price']['options'][0]['formattedDisplayPrice']
        hotel_info = 'отель: ' + str(item['name']) + \
                     '\nадрес: ' + str(data['address']) + \
                     '\nкак далеко расположен от центра (мили): ' + str(data['distanceFromDestination'])
        bot.send_message(message.chat.id, str(count) + '\n' + hotel_info)
        # bot.send_photo(str(item['propertyImage']['image']['url']))
        bot.send_photo(message.chat.id, str(item['propertyImage']['image']['url']),
                       caption='фото в отеле ' + item['name'])
        count += 1
        founded_hotel.append(str(item['name']))
    return payload, founded_hotel, hotel_id_json
