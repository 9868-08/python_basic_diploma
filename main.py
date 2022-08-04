import os
import configparser
import telebot
import requests
from datetime import datetime
import json



class My_json():
    def __init__(self):
        self.datetime = str()
        self.command = str()


def write_log(logfile, to_json):
    with open(logfile, 'w') as f:
        f.write(json.dumps(to_json))



config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("DEFAULT", "TOKEN")
user_id = config.get("DEFAULT", "user_id")
print(TOKEN)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "help":
        bot.send_message(message.from_user.id,
                         " You can use commands:\n help\n lowprice\n highprice\n bestdeal\n history")
    elif message.text == "lowprice":
        bot.send_message(message.from_user.id, "you input - lowprice")
        # bot.send_message(message.from_user.id, lowprice())
    elif message.text == "highprice":
        bot.send_message(message.from_user.id, "you input - highprice")
    elif message.text == "bestdeal":
        bot.send_message(message.from_user.id, "you input - bestdeal")
    elif message.text == "history":
        bot.send_message(message.from_user.id, "you input - history")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю.")


bot.polling(none_stop=True, interval=5)
