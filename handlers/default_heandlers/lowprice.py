from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['lowprice'])
def bot_start(message: Message):
    bot.reply_to(message, f"вывожу список отелей")

