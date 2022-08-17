# import os
import configparser
import telebot
import requests
import json
import asyncio


logfile = "diploma_log.json"
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("DEFAULT", "TOKEN")
user_id = config.get("DEFAULT", "user_id")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
async def show_info(message):
    bot.send_message(message.chat.id, 'Итоговый проект курса «Python Basic» Ермолаева Романа')
    bot.send_message(message.from_user.id, "В каком городе ищем отель?")
    return


@bot.message_handler(content_types=['text'])
async def get_city(message):
    await asyncio.sleep(20)
    city = message.text
    bot.send_message(message.from_user.id, "ищем отель в городе: " + city)

bot.polling(none_stop=True, interval=5)
