import telebot  # telebot
from states import bot_states
from telebot import TeleBot, custom_filters
from telebot.handler_backends import State, StatesGroup  # States
from telebot.storage import StateMemoryStorage
from config_data import config
from states import bot_states


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)


