from aiogram.types.message import Message
from aiogram.utils.exceptions import InvalidHTTPUrlContent, WrongFileIdentifier, BadRequest

from utils.named_tuples import HotelMessage


async def trying_to_send_with_photo(message_from_user: Message, hotel_message: HotelMessage):
    """Tries to send message about hotel with photo. If exception is found sends without photo"""

    try:
        message = await message_from_user.bot.send_photo(chat_id=message_from_user.chat.id, photo=hotel_message.photo,
                                                         caption=hotel_message.text,
                                                         reply_markup=hotel_message.buttons)
    except InvalidHTTPUrlContent:
        message = await message_from_user.answer(text=hotel_message.text, reply_markup=hotel_message.buttons)
    except WrongFileIdentifier:
        message = await message_from_user.answer(text=hotel_message.text, reply_markup=hotel_message.buttons)
    except BadRequest:
        message = await message_from_user.answer(text=hotel_message.text, reply_markup=hotel_message.buttons)

    return message
