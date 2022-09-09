from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

import datetime

from database.history.update_history import add_command_to_history
from photos.work_with_photos import get_photo_by_command
from states.bot_states import SelectCity
from config_data.config import time_offset
from loader import dp


@dp.message_handler(Command(['lowprice', 'highprice', 'bestdeal']), state='*')
async def define_state(message: Message, state: FSMContext):
    """"Catches lowprice and higprice commands. Asks user for city name"""

    command = message.text.lstrip('/')
    await send_city_request_with_photo(message, command)
    await SelectCity.wait_city_name.set()

    await register_command_in_db(command, message, state)


@dp.message_handler(Text(['⬇️ Недорогие отели']), state='*')
async def show_lowprice(message: Message, state: FSMContext):
    """"Catches text about lowprice hotels. Asks user for city name"""

    command = 'lowprice'
    await send_city_request_with_photo(message, command)
    await SelectCity.wait_city_name.set()

    await register_command_in_db(command, message, state)


@dp.message_handler(Text(['⬆️ Дорогие отели']), state='*')
async def show_highprice(message: Message, state: FSMContext):
    """"Catches text about highprice hotels. Asks user for city name"""

    command = 'highprice'
    await send_city_request_with_photo(message, command)
    await SelectCity.wait_city_name.set()

    await register_command_in_db(command, message, state)


@dp.message_handler(Text(['🔍 Поиск с параметрами']), state='*')
async def show_highprice(message: Message, state: FSMContext):
    """"Catches text about hotels with best deal. Asks user for city name"""

    command = 'bestdeal'
    await send_city_request_with_photo(message, command)
    await SelectCity.wait_city_name.set()

    await register_command_in_db(command, message, state)


async def send_city_request_with_photo(message: Message, command: str):
    """Sends request about city to user with decorate photo"""

    await message.bot.send_photo(photo=get_photo_by_command(command=command), chat_id=message.chat.id,
                                 caption='<b>↘️ Отправьте боту город для поиска</b>',
                                 reply_markup=ReplyKeyboardRemove())


async def register_command_in_db(command: str, message: Message, state: FSMContext):
    """Adds called command to db"""

    call_time = datetime.datetime.now(time_offset)

    await add_command_to_history(command=command, call_time=call_time, message=message)
    await state.update_data(command_type=command, command_call_time=call_time)
