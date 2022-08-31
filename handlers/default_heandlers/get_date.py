from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_checkin(message: Message):
    bot.reply_to(message, "Введите дату начала заезда"
                          f"{message.from_user}")
    inc = message.text
    return inc

