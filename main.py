import os
import configparser
import telebot
import requests

config = configparser.ConfigParser()
config.read('config.ini')
token=config.get("DEFAULT", "TOKEN")
#user_id=config.get("DEFAULT", "user_id")
#print(TOKEN, user_id)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "help":
        bot.send_message(message.from_user.id,
                         " You can use commands:\n help\n lowprice\n highprice\n bestdeal\n history")
    elif message.text == "lowprice":
        bot.send_message(message.from_user.id, "you input - lowprice")
#        bot.send_message(message.from_user.id, lowprice())

    elif message.text == "highprice":
        bot.send_message(message.from_user.id, "you input - highprice")
    elif message.text == "bestdeal":
        bot.send_message(message.from_user.id, "you input - bestdeal")
    elif message.text == "history":
        print("you input - history")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю.")


bot.polling(none_stop=True, interval=0)

