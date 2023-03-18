# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config

# from states import bot_states
# from aiogram.dispatcher import Dispatcher

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
# bot = Dispatcher(bot, storage=MemoryStorage())
