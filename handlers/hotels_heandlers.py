from telegram import CallbackQuery

from loader import bot
from states.bot_states import MyStates
# from database import diploma_database
import json
import jsonpickle
from telebot.types import Message
from rapidapi.get_info import city_search
from keyboard.bot_keyboard import makeKeyboard
from keyboard.bot_keyboard import handle_query


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_scenario(message: Message):
    bot.send_message(chat_id=message.from_user.id,
                     text='Введи город поиска'
                     )
    bot.set_state(message.from_user.id, MyStates.city)


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_highprice(message):
    message_dict = json.loads(jsonpickle.encode(message))
    data = dict()
    data['selected_command'] = message_dict['text']
    print(data['selected_command'])
    bot.send_message(message.chat.id, data['selected_command'] + ' was selected. \n Hi, write me a city')

    # diploma_database.Hotel_search(data['selected_command'])
    # request = diploma_database.Hotel_search
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
#    get_checkin.create_calendar(1)
    # create_calendar(callback_data, min_date=None, is_process=None, locale='ru'):
    return


@bot.message_handler(state=MyStates.city)
def city_answer(message: Message):

    with bot.retrieve_data(message.from_user.id) as data: # Сохраняем имя города
        data['city'] = message.text

    cities = city_search(message.text) # Делаем запрос к API
    keyboard = makeKeyboard(cities) # Формируем клавиатуры


    # Отправляем пользователю
    bot.send_message(chat_id=message.from_user.id,
                     text='Уточни выбор:',
                     reply_markup=keyboard
                     )
    bot.set_state(message.from_user.id, MyStates.location_confirmation)


@bot.callback_query_handler(func=None, state=MyStates.location_confirmation)
def location_processing(call_button: CallbackQuery):

    with bot.retrieve_data(call_button.from_user.id) as data: # Сохраняем выбранную локацию
        data['city_id'] = call_button.data

    # Продолжаем диалог
#    bot.send_message(chat_id=call_button.from_user.id,
#                     text='Следующий вопрос',
#                     )
#    bot.set_state(...


@bot.message_handler(state=MyStates.city)
def MyStates_city(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text

    location_dict = rapidapi.get_info.api_request('locations/v3/search', {"q": data['city'], "locale": "ru_RU"}, 'GET')

#    handlers.hotels_heandlers.handle_command_adminwindow(message, location_dict)
    bot.set_state(message.from_user.id, MyStates.city_detail, message.chat.id)
    # bot.set_state(message.from_user.id, MyStates.how_much_hotels, message.chat.id)
    bot.send_message(message.chat.id, 'Now write how much hotels to search')
    return


@bot.message_handler(state=MyStates.how_much_hotels)
def MyStates_how_much_hotels(message):
    bot.send_message(message.chat.id, 'Need photos?')
    bot.set_state(message.from_user.id, MyStates.need_photos, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_hotels'] = message.text


@bot.message_handler(state=MyStates.need_photos)
def MyStates_need_photos(message):
    if message.text == "Y":
        bot.send_message(message.chat.id, 'How much photos?')
        bot.set_state(message.from_user.id, MyStates.print_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text
    else:
        bot.send_message(message.chat.id, 'ok - no photos')
        bot.set_state(message.from_user.id, MyStates.print_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text
            data['need_photos'] = "N"
            data['how_much_photos'] = 0


@bot.message_handler(state=MyStates.print_results)
def print_results(message):
    data = dict()
    data['city'] = "Boston"
    data['how_much_hotels'] = 2
    data['need_photos'] = "Y"
    data['how_much_photos'] = 2

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_photos'] = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"City: {data['city']}\n"
               f"how_much_hotels: {data['how_much_hotels']}\n"
               f"need photos: {data['need_photos']}\n"
               f"how_much_photos: {message.text}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)


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

    hotel_id_json = rapidapi.get_info.api_request('properties/v2/list', payload, 'POST')
    parsed = hotel_id_json['data']['propertySearch']
    hotel_id_list = []
    # import pprint
    count = 0
    for item in parsed['properties']:
        # print (count, int(data['how_much_photos']))
        if count + 1 > int(data['how_much_hotels']):
            break
        hotel_id = int(item['id'])
        # payload = {"currency": "USD", "eapid": 1, "locale": "en_US", "siteId": 300000001, "propertyId": hotel_id}
        hotel_id_list.append(hotel_id)
        print(item['name'])
        #    pprint.pprint(item)
        bot.send_message(message.chat.id, 'найден отель = ' + item['name'])
        # bot.send_photo(str(item['propertyImage']['image']['url']))
        bot.send_photo(message.chat.id, str(item['propertyImage']['image']['url']), caption='фото в отеле ' + item['name'])
        count += 1
    return hotel_id_list
