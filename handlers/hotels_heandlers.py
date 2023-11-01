from builtins import print
from datetime import date
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar
from rapidapi.get_info import api_request
from loader import bot
from states.bot_states import MyStates
import jsonpickle
import json
from database.bot_database import Person, Command, history_put, history_list

ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}  # чтобы русифицировать сообщения


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


def city_markup(cities):
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(
            InlineKeyboardButton(text=city['region_name'],
                                 callback_data=city['id']
                                 )
        )

    return destinations


@bot.message_handler(commands=['history'])
def start_history_scenario(message: Message):
    message_dict = json.loads(jsonpickle.encode(message))
    data = dict()
    data['selected_command'] = message_dict['text']
    bot.send_message(message.chat.id, data['selected_command'] + ' was selected. \n')
    history_list(user_id=message.from_user.id)


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_scenario(message: Message):
    message_dict = json.loads(jsonpickle.encode(message))
    bot.set_state(message.from_user.id, MyStates.city)
    with bot.retrieve_data(message.from_user.id) as data:   # Сохраняем имя города
        data = dict()
        data['city'] = message.text
        data['selected_command'] = message_dict['text']
    bot.send_message(message.chat.id, data['selected_command'] + ' was selected')

    bot.send_message(chat_id=message.from_user.id,
                     text='Введи город поиска'
                     )
    bot.set_state(message.from_user.id, MyStates.city)


@bot.message_handler(state=MyStates.city)
def city_answer(message: Message):
    with bot.retrieve_data(message.from_user.id) as data:   # Сохраняем имя города
        data['city'] = message.text

    cities = city_search(message.text)                      # Делаем запрос к API
    keyboard = city_markup(cities)                          # Формируем клавиатуры

    # Отправляем пользователю
    bot.send_message(chat_id=message.from_user.id,
                     text='Уточните, пожалуйста:',
                     reply_markup=keyboard
                     )
    bot.set_state(message.from_user.id, MyStates.location_confirmation)


@bot.callback_query_handler(func=None, state=MyStates.location_confirmation)
def location_processing(call_button: CallbackQuery):
    with bot.retrieve_data(call_button.from_user.id) as data:  # Сохраняем выбранную локацию
        data['city_id'] = call_button.data
    # формируем календарь
    calendar, step = create_calendar(call_button)
    # отправляем календарь пользователю
    bot.send_message(call_button.from_user.id, f"Укажите {step} заезда", reply_markup=calendar)
    bot.set_state(call_button.from_user.id, MyStates.check_in)


def create_calendar(callback_data, min_date=None, is_process=None, locale='ru'):
    if min_date is None:
        min_date = date.today()

    if is_process:
        result, keyboard, step = DetailedTelegramCalendar(min_date=min_date, locale=locale).process(
            call_data=callback_data.data)
        return result, keyboard, ALL_STEPS[step]
    else:
        calendar, step = DetailedTelegramCalendar(current_date=min_date,
                                                  min_date=min_date,
                                                  locale=locale).build()
        return calendar, ALL_STEPS[step]


@bot.callback_query_handler(func=None, state=MyStates.check_in)
def select_check_in(call_button):
    result, keyboard, step = create_calendar(call_button, is_process=True)
    if not result and keyboard:
        # Продолжаем отсылать шаги, пока не выберут дату "result"
        bot.edit_message_text(f'Укажите {step} заезда',
                              call_button.from_user.id,
                              call_button.message.message_id,
                              reply_markup=keyboard)
    elif result:
        # Дата выбрана, сохраняем и создаем новый календарь с датой отъезда
        with bot.retrieve_data(call_button.from_user.id) as data:  # Сохраняем выбранную локацию
            data['check_in'] = result
        # формируем календарь
        calendar, step = create_calendar(call_button)
        # отправляем календарь пользователю
        bot.send_message(call_button.from_user.id, f"Укажите {step} выезда", reply_markup=calendar)
        bot.set_state(call_button.from_user.id, MyStates.check_out)


@bot.callback_query_handler(func=None, state=MyStates.check_out)
def select_check_out(call_button):
    result, keyboard, step = create_calendar(call_button, is_process=True)
    if not result and keyboard:
        bot.edit_message_text(f'Укажите {step} выезда',
                              call_button.from_user.id,
                              call_button.message.message_id,
                              reply_markup=keyboard)
    elif result:
        with bot.retrieve_data(call_button.from_user.id) as data:
            data['check_out'] = result
        bot.send_message(call_button.from_user.id, 'Введите количество отелей')
        # import telebot
        # from telebot.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardRemove
        bot.set_state(call_button.from_user.id, MyStates.how_much_hotels)
        # Дата выбрана, сохраняем и создаем новый календарь с датой отъезда
        with bot.retrieve_data(call_button.from_user.id) as data:  # Сохраняем выбранную дату заезда
            data['check_in'] = call_button.data
        # формируем календарь
#        calendar, step = create_calendar(call_button)
        # отправляем календарь пользователю
        bot.set_state(call_button.from_user.id, MyStates.how_much_hotels)
#        bot.set_state(call_button.from_user.id, MyStates.how_much_hotels)


@bot.message_handler(state=MyStates.how_much_hotels)
def how_much_hotels(message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['how_much_hotels'] = message.text
    bot.set_state(message.from_user.id, MyStates.print_results)
    print_results(message)
#    bot.send_message(message.from_user.id, 'показать введенные данные?')


# @bot.callback_query_handler(func=None, state=MyStates.print_results)
@bot.message_handler(state=MyStates.print_results)
def print_results(message: Message):
    """
    текстом выводит полученные от пользователя данные
    выводить описание и фотографии найденных отелей в количестве указанном пользователем
    добавить: расстояние от центра
            диапазон цен
    """
    print("runing print_results")
    with bot.retrieve_data(message.from_user.id) as data:
        msg = ("Ready, take a look:\n"
               f"City: {data['city']}\n"
               f"how_much_hotels: {data['how_much_hotels']}")
    bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)

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
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 150,
            "min": 100
        }}
    }
    hotel_id_json = api_request('properties/v2/list', payload, 'POST')
    parsed_dict = hotel_id_json['data']['propertySearch']
    # hotel_id_list = []
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
    return hotel_id_json
