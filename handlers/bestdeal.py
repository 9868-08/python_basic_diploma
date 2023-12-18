from loader import bot
from states import bot_states
from telebot.types import Message
from rapidapi.get_info import api_request
from database.bot_database import (history_put)


@bot.message_handler(state=bot_states.MyStates.bestdeal)
def bestdeal_distance_min(message: Message):
    print("bestdeal running")
    bot.send_message(chat_id=message.from_user.id,
                     text='минимальное расстояние от центра, где будем искать'
                     )
    bot.set_state(message.from_user.id, bot_states.MyStates.bestdeal_distance_min_flag)


@bot.message_handler(state=bot_states.MyStates.bestdeal_distance_min_flag)
def bestdeal_distance_max(message: Message):
    with bot.retrieve_data(message.from_user.id) as data:   # Сохраняем имя города
        data['bestdeal_min'] = message.text
    bot.send_message(chat_id=message.from_user.id,
                     text='максимальное расстояние от центра, где будем искать'
                     )
    bot.set_state(message.from_user.id, bot_states.MyStates.bestdeal_distance_max_flag)


@bot.message_handler(state=bot_states.MyStates.bestdeal_distance_max_flag)
def bestdeal_print_results(message: Message):
    """
    текстом выводит полученные от пользователя данные
    выводить описание и фотографии найденных отелей в количестве указанном пользователем
    добавить: расстояние от центра
            диапазон цен
    """
    print("runing bestdeal print_results")
    with bot.retrieve_data(message.from_user.id) as data:
        msg = ("Ready, take a look:\n"
               f"Command: {data['selected_command']}\n"               
               f"City: {data['city']}\n"
               f"how_much_hotels: {data['how_much_hotels']}")
    bot.send_message(message.chat.id, msg, parse_mode="html")
#    bot.delete_state(message.from_user.id, message.chat.id)
    if data['selected_command'] == '/lowprice':
        bot_sort = 'PRICE_LOW_TO_HIGH'
    elif data['selected_command'] == '/highprice':
        bot_sort = 'PRICE_HIGH_TO_LOW'
    else:
        bot_sort = 'PRICE_LOW_TO_HIGH'
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
    history_put(message.from_user.id, message.from_user.full_name, command=data['selected_command'],
                result=founded_hotel)
    bot.delete_state(message.from_user.id, message.chat.id)
    return hotel_id_json
