from telebot.types import Message
from loader import bot
from states import bot_states
from loader import  bot


@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.bot)
    bot.set_state(message.from_user.id, bot_states.MyStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a city')