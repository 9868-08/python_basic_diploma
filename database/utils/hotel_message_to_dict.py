from aiogram.types.message import Message

#from keyboards.inline.hotel_keyboards.hotel_keyboard import edit_hotel_keyboard_by_favorite
#from keyboards.inline.markup_from_dict import inline_markup_from_dict

from database.utils.utils import is_message_contains_photo, get_photo_id
from utils.named_tuples import HotelMessage


def hotel_dict_from_message(message: Message) -> dict:
    """Converts hotel message to dict with hotel info"""

    is_message_with_photo = is_message_contains_photo(message=message)
    hotel_dict = {
        'photo_id': get_photo_id(message) if is_message_with_photo else 'link_not_found',
        'text': message.caption if is_message_with_photo else message.text,
        'keyboard': dict(edit_hotel_keyboard_by_favorite(message.reply_markup, is_favorite=True))
    }
    return hotel_dict


def hotel_message_from_hotel_dict(hotel_info: dict) -> HotelMessage:
    """Converts dict with hotel info to hotel message"""

    return HotelMessage(
        text=hotel_info.get('text'),
        photo=hotel_info.get('photo_id'),
        buttons=inline_markup_from_dict(hotel_info.get('keyboard'))
    )
