# import os
import configparser
import telebot
import requests
# from datetime import datetime
# import json
import json
import asyncio
from datetime import datetime
import handlers


class My_json:
    def __init__(self):
        self.datetime = str()
        self.command = str()

    def __str__(self):
        return str(self.datetime) + "\t\t" + str(self.command)

    @staticmethod
    def append(str_to_append):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        to_append_dict = dict()
        to_append_dict[date_time] = str_to_append
        with open(logfile, 'a') as f:
            json.dump(to_append_dict, f, indent=4)  # сериализация JSON
        f.close()


def append(str_to_append):
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    to_append_dict = dict()
    to_append_dict[date_time] = str_to_append
    #    print(to_append_dict)
    with open(logfile, 'a') as f:
        print("to_append_dict=", to_append_dict, "logfile=", logfile)
        json.dump(to_append_dict, f, indent=4)  # сериализация JSON
    f.close()


'''def hotels_requiest():          # запрос списка всех отелей без сортировки
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": "new york", "locale": "en_US", "currency": "RUB"}
    headers = {
        "X-RapidAPI-Key": "a66df32f87mshe86994164d3c458p18029djsnb52f634dfcfe",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #    print(response.text)
    return response.text'''


def hotels_requiest_highprice(def_city, count):  # запрос списка всех отелей c сортировкой по цене сперва дорогие
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": "1506246", "pageNumber": "1", "pageSize": "25", "checkIn": "<REQUIRED>",
                   "checkOut": "<REQUIRED>", "adults1": "1", "sortOrder": "PRICE_HIGHEST_FIRST", "locale": "en_US",
                   "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": "a66df32f87mshe86994164d3c458p18029djsnb52f634dfcfe",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response.text


my_json = My_json()
logfile = "diploma_log.json"
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("DEFAULT", "TOKEN")
user_id = config.get("DEFAULT", "user_id")
bot = telebot.TeleBot(TOKEN)

'''@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "help":
       bot.send_message(message.from_user.id,
                         " You can use commands:\n help\n lowprice\n highprice\n bestdeal\n history")
    elif message.text == "lowprice":
        bot.send_message(message.from_user.id, "you input - lowprice")
        all_hotels_str = hotels_requiest()
        all_hotels_dict = eval(all_hotels_str)
        my_json.append(("lowprice command", all_hotels_dict))
    elif message.text == "highprice":
        append("highprice")
        bot.send_message(message.from_user.id, "you input - highprice")
    elif message.text == "bestdeal":
        bot.send_message(message.from_user.id, "you input - bestdeal")
    elif message.text == "history":
        bot.send_message(message.from_user.id, "you input - history")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю.")
'''


@bot.message_handler(Command(['lowprice', 'highprice', 'bestdeal']), state='*')
async def define_state(message: Message, state: FSMContext):
    """"Catches lowprice and higprice commands. Asks user for city name"""

    command = message.text.lstrip('/')
    await send_city_request_with_photo(message, command)
    await SelectCity.wait_city_name.set()

    await register_command_in_db(command, message, state)



@bot.message_handler(content_types=['text'])
def main(message):
    bot.send_message(message.from_user.id, "В каком городе ищем отель?")
    city = message.text
    bot.send_message(message.from_user.id, "ищем отель в городе: " + city)
    city = "New   york"
    bot.send_message(message.from_user.id, "для отладки ищем отель в городе: " + city)
    return city

    bot.send_message(message.from_user.id, "The check-in date at hotel, formated as yyyy-MM-dd:")
    checkIn = message.text
    bot.send_message(message.from_user.id, "The check-out date at hotel, formated as yyyy-MM-dd:")
    checkOut = message.text
    bot.send_message(message.from_user.id, "Выбран город " + city + " с " + checkIn + "по" + checkOut)



bot.send_message(message.from_user.id, "you input - highprice")
bot.polling(none_stop=False, interval=5)
bot.send_message(message.from_user.id, "для отладки ищем отель в городе: " + city)

