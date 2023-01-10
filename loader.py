#from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from config_data import config
from states import bot_states
#from aiogram.dispatcher import Dispatcher

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
#bot = Dispatcher(bot, storage=MemoryStorage())


@bot.message_handler(state='*', commands=['lowprice'])
def help (message):
    bot.set_state(message.from_user.id,bot_states.MyStates.lowprice, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, ищем самые дешовые отелы и городе %город%')


@bot.message_handler(state='*', commands=['highprice'])
def help(message):
    bot.set_state(message.from_user.id, bot_states.MyStates.highprice, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, ищем самые дорогие отелы и городе %город%')


@bot.message_handler(state='*', commands=['bestdeal'])
def help(message):
    bot.set_state(message.from_user.id, bot_states.MyStates.bestdeal, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, ищем самые дорогие отелы и городе %город%')


@bot.message_handler(state='*', commands=['history'])
def help(message):
    bot.set_state(message.from_user.id, bot_states.MyStates.history, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, ищем самые дорогие отелы и городе %город%')

