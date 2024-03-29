from loader import bot
from states.bot_states import MyStates
from telebot.types import Message
from rapidapi.get_info import api_request
from database.bot_database import (history_put)


# запрос от пользователя минимального растяния от центра
@bot.message_handler(state=MyStates.bestdeal_distance_min_flag)
def bestdeal_distance_min(message: Message):
    """asks min distance from center to hotel"""
    print("bestdeal_distance_min running")
    with bot.retrieve_data(message.from_user.id) as data:   # Сохраняем имя города
        data['how_much_hotels'] = message.text
    bot.send_message(chat_id=message.from_user.id,
                     text='минимальное расстояние от центра, где будем искать'
                     )
    bot.set_state(message.from_user.id, MyStates.bestdeal_distance_max_flag)


# запрос от пользователя максимального растяния от центра
@bot.message_handler(state=MyStates.bestdeal_distance_max_flag)
def bestdeal_distance_max(message: Message):
    """asks max distance from center to hotel"""
    print("bestdeal_distance_max running")
    with bot.retrieve_data(message.from_user.id) as data:   # Сохраняем имя города
        data['bestdeal_min'] = message.text
    bot.send_message(chat_id=message.from_user.id,
                     text='максимальное расстояние от центра, где будем искать'
                     )
    bot.set_state(message.from_user.id, MyStates.bestdeal_print_results)
    return


# отправить в телеграм все отели с заданными параметрами
@bot.message_handler(state=MyStates.bestdeal_print_results)
def bestdeal_print_results(message: Message):
    """
    текстом выводит полученные от пользователя данные
    выводить описание и фотографии найденных отелей в количестве указанном пользователем
    """
    print("runing bestdeal print_results")
#    bot.delete_state(message.from_user.id, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['bestdeal_max'] = message.text
        msg = ("Ready, take a look:\n"
               f"Command: {data['selected_command']}\n"               
               f"City: {data['city']}\n"
               f"how_much_hotels: {data['how_much_hotels']}\n"
               f"bestdeal_distance_min: {data['bestdeal_min']}\n"
               f"bestdeal_distance_max: {data['bestdeal_max']}\n"
               )
    bot.send_message(message.chat.id, msg, parse_mode="html")
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": "6054439"},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2023
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2023
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": 'DISTANCE',
        "filters": {"DISTANCE": {
            "max": data['bestdeal_max'],
            "min": data['bestdeal_min']

        }}
    }
    hotel_id_json = api_request('properties/v2/list', payload, 'POST')
    parsed_dict = hotel_id_json['data']['propertySearch']

    # hotel_id_list = []
    founded_hotel = []
    count = 1
    for item in parsed_dict['properties']:
        if not item['destinationInfo']['distanceFromDestination']['value'] > float(data['bestdeal_min']):
            continue
        if item['destinationInfo']['distanceFromDestination']['value'] > float(data['bestdeal_max']):
            break
        if count > int(data['how_much_hotels']):
            break
        data['distanceFromDestination'] = item['destinationInfo']['distanceFromDestination']['value']
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": item['id']
        }  # дефолтые значения с сайта
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
        print("bestdeal_print_results finished")
    history_put(message.from_user.id, message.from_user.full_name, command=data['selected_command'],
                result=founded_hotel)
    bot.delete_state(message.from_user.id, message.chat.id)
    return hotel_id_json
