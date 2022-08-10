import os
import configparser
import telebot
import requests
from datetime import datetime
import json
from datetime import datetime
import json
from datetime import datetime


class My_json():
    def __init__(self):
        self.datetime = str()
        self.command = str()

    def __str__(self):
        return str(self.datetime) + "\t\t" + str(self.command)

    def append(self, str_to_append):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        to_append_dict = dict()
        to_append_dict[date_time] = str_to_append
        print(to_append_dict)
        with open(logfile, 'a') as f:
            print("to_append_dict=", to_append_dict, "logfile=", logfile)
            json.dump(to_append_dict, logfile, indent=4)  # сериализация JSON
        f.close()


def append(str_to_append):
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    to_append_dict = dict()
    to_append_dict[date_time] = str_to_append
    print(to_append_dict)
    with open(logfile, 'a') as f:
        print("to_append_dict=", to_append_dict, "logfile=", logfile)
        json.dump(to_append_dict, f, indent=4)  # сериализация JSON
    f.close()


my_json = My_json()
logfile = "diploma_log.json"
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("DEFAULT", "TOKEN")
user_id = config.get("DEFAULT", "user_id")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "help":
        bot.send_message(message.from_user.id,
                         " You can use commands:\n help\n lowprice\n highprice\n bestdeal\n history")
    elif message.text == "lowprice":
        bot.send_message(message.from_user.id, "you input - lowprice")
        my_json.append("lowprice")
        bot.send_message(message.from_user.id, "you input - lowprice 2")
    elif message.text == "highprice":
        append("highprice")
        bot.send_message(message.from_user.id, "you input - highprice")
    elif message.text == "bestdeal":
        bot.send_message(message.from_user.id, "you input - bestdeal")
    elif message.text == "history":
        bot.send_message(message.from_user.id, "you input - history")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю.")


bot.polling(none_stop=True, interval=5)
