from loader import  bot

# import os
from telebot.custom_filters import StateFilter
import configparser
import telebot
import requests
import json
from datetime import datetime
import requests
#import handlers


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


def request_to_api(url, headers, querystring):
    try:
        # url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        # querystring = {"query": "def_city", "locale": "en_US", "currency": "USD"}
        # headers = {
          #   "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
          #   "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        #}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == requests.codes.ok:
            return response
    except Exception as e:
        print(response.text)

# Получение сообщений от юзера
@bot.message_handler(content_types=["help"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "help":
       bot.send_message(message.from_user.id,
                         " You can use commands:\n help\n lowprice\n highprice\n bestdeal\n history")
    elif message.text == "lowprice":
        bot.send_message(message.chat.id, "Введите дату заезда в формате YYYY-MM-DD")
        checkin = message.text
        bot.send_message(message.chat.id, "Введите дату выезда в формате YYYY-MM-DD")
        checkout = message.text
        bot.send_message(message.chat.id, "Введите город")
        city = message.text
        result = "вы хотите поехать в "+city+" c "+checkin+" по "+checkout
        bot.send_message(message.from_user.id, result)

        bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
        #checkIn = bot.
        all_hotels_str = request_to_api(
            "https://hotels4.p.rapidapi.com/properties/list",
            {
                "X-RapidAPI-Key": "a66df32f87mshe86994164d3c458p18029djsnb52f634dfcfe",
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            },
            {"destinationId": "1506246", "pageNumber": "1", "pageSize": "25", "checkIn": "2022-12-10",
             "checkOut": "2022-12-15", "adults1": "1", "sortOrder": "PRICE", "locale": "en_US", "currency": "USD"}
            )
        all_hotels_json = json.loads(all_hotels_str.text)  # десериализация JSON
        print(type(all_hotels_json))

        my_json.append(("lowprice command", all_hotels_json))
        bot.send_message(message.from_user.id, all_hotels_json)

    elif message.text == "highprice":
        bot.send_message(message.from_user.id, "you input - highprice")
    elif message.text == "bestdeal":
        bot.send_message(message.from_user.id, "you input - bestdeal")
    elif message.text == "history":
        bot.send_message(message.from_user.id, "you input - history")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю.")


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


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
    '''     my_json = My_json()
    logfile = "diploma_log.json"
    config = configparser.ConfigParser()
    config.read('config.ini')
    TOKEN = config.get("DEFAULT", "TOKEN")
    user_id = config.get("DEFAULT", "user_id")
    bot = telebot.TeleBot(TOKEN)
    bot.polling(none_stop=False, interval=5)
'''
