from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config_data import config
from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram import executor
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import bot
from loader import dp


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
print(dp)


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nhelp replay")



@dp.message_handler(state=None, content_types=ContentTypes.ANY)
async def bot_echo(message: Message):
    """Heandler that takes messages without a filter or state"""

    await message.answer("сам такой!!! Эхо без состояния или фильтра."
                         f"\nСообщение: {message.text}")

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