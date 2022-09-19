from aiogram.types.message import Message
from database.connect_to_db.client import get_favorites_collection
from database.utils.utils import get_hotel_id


async def delete_from_favorites(message: Message):
    """Deletes hotel from favorites by hotel id (gets from message)"""

    collection = get_favorites_collection()
    user = await collection.find_one({'_id': message.chat.id})
    user_favorites: dict = user['favorites']

    del user_favorites[get_hotel_id(message.reply_markup)]

    await collection.update_one({'_id': message.chat.id}, {'$set': {'favorites': user_favorites}})
