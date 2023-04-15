import telebot
import constants
from telebot import types
from loader import bot


@bot.message_handler(commands=["command"])  # В commands может быть несколько разных команд
def answer(message):
    command = message.split(maxsplit=1)[1]  # В переменной будет всё,что идёт после /command
