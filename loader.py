# from telebot import TeleBot
# from telebot.storage import StateMemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config_data import config


#storage = StateMemoryStorage()
#bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)