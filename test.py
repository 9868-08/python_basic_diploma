from loader import bot
import telegram
from telebot.types import Message, CallbackQuery


bot.send_message(message.chat.id, msg, parse_mode="html")

# bot.send_message(chat_id=chat_id, text="*bold* Example message",
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

# bot.send_message(chat_id=chat_id, text='<b>Example message</b>',
                  parse_mode=telegram.ParseMode.HTML)