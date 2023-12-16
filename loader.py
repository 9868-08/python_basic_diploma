# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
import config_data

# from states import bot_states
# from aiogram.dispatcher import Dispatcher
from config_data.config import BOT_TOKEN

storage = StateMemoryStorage()
bot = TeleBot(token=BOT_TOKEN, state_storage=storage)
# bot = Dispatcher(bot, storage=MemoryStorage())
