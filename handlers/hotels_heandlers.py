from requests import get, codes
from requests.exceptions import ConnectTimeout
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import bot
from states.bot_states import MyStates


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
    try:
        response = get(
            url,
            headers={  # TODO Ваш словарик с ключом доступа
                "X-RapidAPI-Key": "c7ca9cdd48msh13b9bab2e4955ffp1b87f9jsncf0790864cbc",
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            },
            params=params,
            timeout=15
        )
        if response.status_code == codes.ok:
            return response.json()
    except ConnectTimeout as error:  # TODO Так как указали таймаут может быть прокинута ошибка - from requests.exceptions import ConnectTimeout
        print(error)  # TODO Что-то делаем при возникновении ошибки


def city_search(city_name):
    query_string = {'q': city_name, 'locale': 'ru_RU'}
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


def city_markup(cities):
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(
            InlineKeyboardButton(text=city['region_name'],
                                 callback_data=city['id']
                                 )
        )

    return destinations


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_scenario(message: Message):
    bot.send_message(chat_id=message.from_user.id,
                     text='Введи город поиска'
                     )
    bot.set_state(message.from_user.id, MyStates.city)


@bot.message_handler(state=MyStates.city)
def city_answer(message: Message):
    with bot.retrieve_data(message.from_user.id) as data:  # TODO Сохраняем имя города
        data['city'] = message.text

    cities = city_search(message.text)  # TODO Делаем запрос к API
    keyboard = city_markup(cities)  # TODO Формируем клавиатуры

    # TODO Отправляем пользователю
    bot.send_message(chat_id=message.from_user.id,
                     text='Уточните, пожалуйста:',
                     reply_markup=keyboard
                     )
    bot.set_state(message.from_user.id, MyStates.location_confirmation)


@bot.callback_query_handler(func=None, state=MyStates.location_confirmation)
def location_processing(call_button: CallbackQuery):
    with bot.retrieve_data(call_button.from_user.id) as data:  # TODO Сохраняем выбранную локацию
        data['city_id'] = call_button.data

    # TODO Продолжаем диалог
    bot.send_message(chat_id=call_button.from_user.id,
                     text='Сколько отелей показать?',
                     )
    bot.set_state(message.from_user.id, MyStates.how_much_hotels)


@bot.message_handler(state=MyStates.how_much_hotels)
def MyStates_how_much_hotels(message):
    bot.send_message(message.chat.id, 'Need photos?')
    bot.set_state(message.from_user.id, MyStates.need_photos, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_hotels'] = message.text


# @bot.message_handler(state=MyStates.need_photos)
# def MyStates_need_photos(message):
#     if message.text == "Y":
#         bot.send_message(message.chat.id, 'How much photos?')
#         bot.set_state(message.from_user.id, MyStates.print_results, message.chat.id)
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['need_photos'] = message.text
#     else:
#         bot.send_message(message.chat.id, 'ok - no photos')
#         bot.set_state(message.from_user.id, MyStates.print_results, message.chat.id)
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['need_photos'] = message.text
#             data['need_photos'] = "N"
#             data['how_much_photos'] = 0
#
#
# @bot.message_handler(state=MyStates.print_results)
# def print_results(message):
#     data = dict()
#     data['city'] = "Boston"
#     data['how_much_hotels'] = 2
#     data['need_photos'] = "Y"
#     data['how_much_photos'] = 2
#
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['how_much_photos'] = message.text
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         msg = ("Ready, take a look:\n<b>"
#                f"City: {data['city']}\n"
#                f"how_much_hotels: {data['how_much_hotels']}\n"
#                f"need photos: {data['need_photos']}\n"
#                f"how_much_photos: {message.text}</b>")
#         bot.send_message(message.chat.id, msg, parse_mode="html")
#     bot.delete_state(message.from_user.id, message.chat.id)
#
#     payload = {
#         "currency": "USD",
#         "eapid": 1,
#         "locale": "ru_RU",
#         "siteId": 300000001,
#         "destination": {"regionId": location_id},
#         "checkInDate": {
#             "day": 10,
#             "month": 10,
#             "year": 2022
#         },
#         "checkOutDate": {
#             "day": 15,
#             "month": 10,
#             "year": 2022
#         },
#         "rooms": [
#             {
#                 "adults": 2,
#                 "children": [{"age": 5}, {"age": 7}]
#             }
#         ],
#         "resultsStartingIndex": 0,
#         "resultsSize": 200,
#         "sort": "PRICE_LOW_TO_HIGH",
#         "filters": {"price": {
#             "max": 150,
#             "min": 100
#         }}
#     }
#
#     hotel_id_json = api_request('properties/v2/list', payload, 'POST')
#     parsed = hotel_id_json['data']['propertySearch']
#     hotel_id_list = []
#     # import pprint
#     count = 0
#     for item in parsed['properties']:
#         # print (count, int(data['how_much_photos']))
#         if count + 1 > int(data['how_much_hotels']):
#             break
#         hotel_id = int(item['id'])
#         # payload = {"currency": "USD", "eapid": 1, "locale": "en_US", "siteId": 300000001, "propertyId": hotel_id}
#         hotel_id_list.append(hotel_id)
#         print(item['name'])
#         #    pprint.pprint(item)
#         bot.send_message(message.chat.id, 'найден отель = ' + item['name'])
#         # bot.send_photo(str(item['propertyImage']['image']['url']))
#         bot.send_photo(message.chat.id, str(item['propertyImage']['image']['url']), caption='фото в отеле ' + item['name'])
#         count += 1
#     return hotel_id_list
