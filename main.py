# import sys
from loader import bot
# from utils.set_bot_commands import set_default_commands
from telebot import custom_filters
# import handlers
# from handlers import bestdeal
from handlers import hotels_handlers
# from loguru import logger
# import logging
# import mk_telegram_inline_keyboard

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

print("main started")
if __name__ == '__main__':
    # set_default_commands(bot)
    bot.infinity_polling(skip_pending=True)
