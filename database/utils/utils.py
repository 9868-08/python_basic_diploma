from aiogram.types.message import Message
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from database.connect_to_db.client import get_favorites_collection
#from keyboards.inline.hotel_keyboards.hotel_keyboard import edit_hotel_keyboard_by_favorite

from utils.named_tuples import HotelMessage


def is_message_contains_photo(message: Message) -> bool:
    return True if message.photo else False


def get_photo_id(message: Message) -> str:
    return message.photo[-1]['file_id']


def get_hotel_id(inline_markup: InlineKeyboardMarkup) -> str:
    """Returns hotel id by inline keyboard of sended message"""

    link_button: InlineKeyboardButton = inline_markup.inline_keyboard[0][0]
    link = link_button.url

    hotel_id = link.lstrip('http://hotels.com/ho')
    return hotel_id


async def is_favorites_are_over(message: Message) -> bool:
    """Checks is favorite hotels are over"""

    collection = get_favorites_collection()
    user: dict = await collection.find_one({'_id': message.chat.id})

    if not user:
        return True
    if not user['favorites']:
        return True

    return False


async def get_correct_hotel_info_by_favorites(user_id, hotel: HotelMessage) -> HotelMessage:
    """
    Returns correct info about hotel. Checks if hotel is favorite.
    Use for resolving conflicts with history entry and favorite entry of one hotel
    """

    collection = get_favorites_collection()

    user = await collection.find_one({'_id': user_id})
    user_favorites: dict = user['favorites']
    if get_hotel_id(hotel.buttons) in user_favorites:
        return hotel
    else:
        return HotelMessage(text=hotel.text,
                            photo=hotel.photo,
                            buttons=edit_hotel_keyboard_by_favorite(hotel.buttons, is_favorite=False))
