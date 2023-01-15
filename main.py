from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging


def on_startup(dispatcher):
    logger = logging.getLogger(__name__)

    dispatcher.setup_middleware(LoggingMiddleware())
    logger.info("Starting bot")
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    set_default_commands(dispatcher)


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
    #executor.start_polling(dp, on_startup=on_startup)

