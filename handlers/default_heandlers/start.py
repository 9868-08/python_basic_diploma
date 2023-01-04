from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.name, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a name')