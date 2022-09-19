from aiogram.types.message import Message
from motor.motor_asyncio import AsyncIOMotorCollection

from database.connect_to_db.client import get_history_collection
from database.utils.hotel_message_to_dict import hotel_dict_from_message
from utils.misc.work_with_dates import get_readble_date_time


async def add_hotel_to_history(message: Message, call_time):
    """Adds hotel to user history in db. Adds to history page by time when command was called"""

    collection = get_history_collection()

    user = await collection.find_one({'_id': message.chat.id})
    if user:
        history = user['history']
    else:
        history = dict()
        history[str(call_time)]['found_hotels'] = list()

    current_history_page: list = history[str(call_time)]['found_hotels']
    current_history_page.append(hotel_dict_from_message(message))

    await collection.update_one({'_id': message.chat.id}, {'$set': {'history': history}})


async def add_command_to_history(command: str, call_time, message: Message):
    """Adds called command to db, by time when command was called """

    collection = get_history_collection()
    user = await collection.find_one({'_id': message.chat.id})
    if user:
        await add_new_to_history(user, collection, command, str(call_time), message)
    else:
        await create_history(collection, command, str(call_time), message)


async def add_new_to_history(user: dict, collection: AsyncIOMotorCollection, command: str, call_time: str,
                             message: Message):
    """Adds command to history if user exists in db"""

    user_history = user['history']
    user_history_page = create_history_dict(command=command, call_time=call_time)
    user_history[call_time] = user_history_page

    await collection.update_one({'_id': message.chat.id}, {'$set': {'history': user_history}})


async def create_history(collection: AsyncIOMotorCollection, command: str, call_time: str, message: Message):
    """Creates user history entry in db. Adds command to user history in db"""

    user_history_page = create_history_dict(command=command, call_time=call_time)

    await collection.insert_one({'_id': message.chat.id, 'history': {call_time: user_history_page}})


def create_history_dict(command: str, call_time: str) -> dict:
    """Creates history entry by command and time when command was called"""

    history_dict = {
        'text': f'<b>Команда</b> /{command} вызвана\n'
                f'в {get_readble_date_time(call_time)}',
        'found_hotels': []
    }

    return history_dict


async def add_city_to_history(city: str, call_time: str, user_id: str):
    """Adds name of the selected city to text in history page"""

    collection = get_history_collection()
    user = await collection.find_one({'_id': user_id})

    user_history: dict = user['history']
    history_page: dict = user_history[call_time]
    text_to_edit = history_page.get('text')

    text_with_city = f'Поиск в городе <b>{city}</b>\n' + text_to_edit
    history_page['text'] = text_with_city

    await collection.update_one({'_id': user_id}, {'$set': {'history': user_history}})
