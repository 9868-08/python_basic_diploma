import logging

from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message, ContentTypes

from config_data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
print(dp)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\n"
                        "\help', "Вывести справку"),
    ('lowprice',  'Узнать топ самых дешёвых отелей в городе'),
    ('highprice', 'Узнать топ самых дорогих отелей в городе'),
    ('bestdeal',  'Узнать топ отелей, наиболее подходящих по цене и расположению от центра (самые дешёвые и находятся ближе всего к центру)'),
    ('history',   'Узнать историю поиска отелей')")
    await message.reply("await message.reply")


async def on_startup(dispatcher):
    logger = logging.getLogger(__name__)

    dispatcher.setup_middleware(LoggingMiddleware())
    logger.info("Starting bot")
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

#    await set_default_commands(dispatcher)

executor.start_polling(dp, on_startup=on_startup)