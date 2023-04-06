import sys
#from asyncore import dispatcher

from loader import bot
#from utils.set_bot_commands import set_default_commands
from telebot import custom_filters
import handlers
from loguru import logger
import logging

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())



if __name__ == '__main__':
#    set_default_commands(bot)
    bot.infinity_polling(skip_pending=True)
