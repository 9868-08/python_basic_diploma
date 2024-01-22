from builtins import print
from datetime import date
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar

import rapidapi.rapidapi_payload
from loader import bot
from states.bot_states import MyStates
import jsonpickle
import json
from database.bot_database import (history_put, history_list)
from rapidapi.work_with_city import city_search
from keyboard.bot_keyboard import city_markup
from rapidapi.rapidapi_payload import bot_payload
# import handlers
ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}  # чтобы русифицировать сообщения


@bot.message_handler(commands=['history'])
def start_history_scenario(message: Message):
    message_dict = json.loads(jsonpickle.encode(message))
    data = dict()
    data['selected_command'] = message_dict['text']
    bot.send_message(message.chat.id, data['selected_command'] + ' was selected. \n')
    history = history_list(user_telegram_id=message.from_user.id)
    for i in history:
        result = ''
        for j in i:
            print(j, end=' ')
            result = result + str(j) + "  "
        bot.send_message(message.chat.id, str(result) + '\n')


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_scenario(message: Message):
    message_dict = json.loads(jsonpickle.encode(message))
    bot.set_state(message.from_user.id, MyStates.city)
    with bot.retrieve_data(message.from_user.id) as data:
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

    bot.set_state(message.from_user.id, MyStates.location_confirmation)
    # Отправляем пользователю
    bot.send_message(chat_id=message.from_user.id,
                     text='Уточните, пожалуйста:',
                     reply_markup=keyboard
                     )


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
        bot.set_state(call_button.from_user.id, MyStates.check_out)
        # формируем календарь
        calendar, step = create_calendar(call_button)
        # отправляем календарь пользователю
        bot.send_message(call_button.from_user.id, f"Укажите {step} выезда", reply_markup=calendar)


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
            if data['selected_command'] == "/bestdeal":
                # Если bestdeal, то состояние MyStates.bestdeal_distance_min_flag
                bot.set_state(call_button.from_user.id, MyStates.bestdeal_distance_min_flag)
            else:
                # В другом случае MyStates.how_much_hotels
                bot.set_state(call_button.from_user.id, MyStates.how_much_hotels)
        bot.send_message(call_button.from_user.id, 'Введите количество отелей')
    return


@bot.message_handler(state=MyStates.how_much_hotels)
def how_much_hotels(message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['how_much_hotels'] = message.text
    bot.set_state(message.from_user.id, MyStates.print_results)
    if data['selected_command'] != '/bestdeal':
        print_results(message)


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
               f"Command: {data['selected_command']}\n"
               f"City: {data['city']}\n"
               f"how_much_hotels: {data['how_much_hotels']}")
    bot.send_message(message.chat.id, msg, parse_mode="html")
#    bot.delete_state(message.from_user.id, message.chat.id)
    bot_sort = ""
    if data['selected_command'] == '/lowprice':
        bot_sort = 'PRICE_LOW_TO_HIGH'
    elif data['selected_command'] == '/highprice':
        bot_sort = 'PRICE_HIGH_TO_LOW'
    elif data['selected_command'] == '/bestdeal':
        bot_sort = 'DISTANCE'
        bot.set_state(message.from_user.id, MyStates.bestdeal)
        bot.send_message(chat_id=message.from_user.id,
                         text='минимальное расстояние от центра, где будем искать'
                         )
        return
    payload, founded_hotel, hotel_id_json = rapidapi.rapidapi_payload.bot_payload(message)

    history_put(message.from_user.id, message.from_user.full_name, command=data['selected_command'],
                result=founded_hotel)
    bot.delete_state(message.from_user.id, message.chat.id)
    return hotel_id_json
