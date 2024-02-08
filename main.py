from loader import bot
from telebot import custom_filters
import handlers
# from loguru import logger
# import logging

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())


print("main started")
if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
