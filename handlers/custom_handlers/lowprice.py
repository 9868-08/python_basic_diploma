#from telebot.types import Message
#from handlers.default_heandlers.get_date import bot_checkin
#from loader import bot

checkin = bot_checkin(bot)


@bot.message_handler(commands=['lowprice'])
def bot_start(message: Message):
    bot.reply_to(message, "выбрана дата - "
                          f"{checkin}")
    bot.reply_to(message, f"выбрана дата - ")
    bot.reply_to(message, f"вывожу список отелей")

