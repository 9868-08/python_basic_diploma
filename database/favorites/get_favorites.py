from aiogram.types.message import Message

from database.connect_to_db.client import get_favorites_collection
from database.utils.hotel_message_to_dict import hotel_message_from_hotel_dict

from utils.named_tuples import HotelMessage


'''async def get_favorite_hotels(message: Message) -> list[HotelMessage]:
    """Returns list of user favorite hotels from db"""

    found_hotels: dict = await find_favorite_hotels_in_db(user_id=message.chat.id)
    hotel_messages: list[HotelMessage] = parse_favorite_hotels_info(hotels=found_hotels)

    return hotel_messages'''


async def find_favorite_hotels_in_db(user_id: int) -> dict:
    """Finds user favorite hotels in db"""

    collection = get_favorites_collection()

    user: dict = await collection.find_one({'_id': user_id})
    if user:
        return user['favorites']
    return {}


def parse_favorite_hotels_info(hotels: dict) -> list[HotelMessage]:
    """Returns list of favorite hotel messages by found favorites"""

    hotel_messages = list()

    for hotel_info in hotels.values():
        hotel_messages.append(hotel_message_from_hotel_dict(hotel_info))

    return hotel_messages
