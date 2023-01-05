import telebot  # telebot
from states import bot_states
from telebot import TeleBot, custom_filters
from telebot.handler_backends import State, StatesGroup  # States
from telebot.storage import StateMemoryStorage
from config_data import config
from states import bot_states
from loader import bot


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def city_requiest (message):
    global mycity
    mycity = ""
    bot.set_state(message.from_user.id,bot_states.MyStates.far_away_from_center, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a target city')
    mycity = message.text
    print("city=", mycity)


@bot.message_handler(state=bot_states.MyStates.far_away_from_center)
def name_get(message):
    bot.send_message(message.chat.id, 'How far away from center?')
    bot.delete_state(message.from_user.id, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text

