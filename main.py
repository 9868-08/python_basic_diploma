from aiogram import executor
import bot
from utils.set_bot_commands import set_default_commands
import logging
from loader import dp

from handlers import default_handlers


async def on_startup(dispatcher):
    logger = logging.getLogger(__name__)

    dispatcher.setup_middleware(LoggingMiddleware())
    logger.info("Starting bot")
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
