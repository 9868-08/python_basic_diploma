from aiogram.dispatcher import FSMContext
from aiogram.types.input_media import InputMediaPhoto
from aiogram.types.callback_query import CallbackQuery, Message

from rapidapi.parse_responses.find_hotels_and_photos import get_hotel_photo_links

from utils.named_tuples import Link, ID
from utils.work_with_messages.search_waiting import send_waiting_message, del_waiting_messages
from utils.misc.work_with_errors import is_message_error, finish_with_error

from keyboards.inline.hotel_keyboards.hotel_keyboard import create_map_keyboard, create_photos_keyboard

from loader import dp, bot


@dp.callback_query_handler(lambda call: call.data.startswith('get_hotel_map'), state='*')
async def get_hotel_map(call: CallbackQuery):
    """Sends hotel geoposition on map as telegram location object. Has two links to popular maps apps"""

    latitude, longitude = map(float, call.data.lstrip('get_hotel_map').split('/'))
    await bot.send_location(chat_id=call.message.chat.id, latitude=latitude, longitude=longitude,
                            reply_markup=create_map_keyboard(latitude, longitude))


@dp.callback_query_handler(lambda call: call.data.startswith('get_hotel_photos'), state='*')
async def get_hotel_photos(call: CallbackQuery, state: FSMContext):
    """Searches photos of the hotel and sends first of them in paginator message"""

    text_to_delete, sticker_to_delete = await send_waiting_message(call.message)

    hotel_id: ID = int(call.data.lstrip('get_hotel_photos'))
    photo_links: list[Link] = await get_hotel_photo_links(hotel_id)
    if is_message_error(photo_links):
        await finish_with_error(call.message, state,
                                error=photo_links.get('error'), to_delete=(text_to_delete, sticker_to_delete))
        return

    await state.update_data(photos=photo_links)

    await del_waiting_messages(text_to_delete, sticker_to_delete)
    await send_hotel_photo(message=call.message, found_photos=photo_links)


@dp.callback_query_handler(lambda call: call.data.startswith('get_photo'), state='*')
async def show_hotel_photo(call: CallbackQuery, state: FSMContext):
    """Goes to next page with photo in paginator message"""

    photo_index = int(call.data.lstrip('get_photo'))
    state_data = await state.get_data()
    photos = state_data.get('photos')

    await send_new_hotel_photo(message=call.message, found_photos=photos, photo_index=photo_index)


async def send_hotel_photo(message: Message, found_photos: list[Link]):
    """Sends first photo of the hotel"""

    await bot.send_photo(chat_id=message.chat.id,
                         photo=found_photos[0],
                         reply_markup=create_photos_keyboard(len(found_photos)))


async def send_new_hotel_photo(message: Message, found_photos: list, photo_index: int = 1):
    """Edits paginator message with photo of the hotel by page number"""

    await bot.edit_message_media(chat_id=message.chat.id,
                                 message_id=message.message_id,
                                 media=InputMediaPhoto(found_photos[photo_index - 1]),
                                 reply_markup=create_photos_keyboard(len(found_photos), page=photo_index))


@dp.callback_query_handler(lambda call: call.data == 'close_message', state='*')
async def close_message(call: CallbackQuery):
    """Deletes message. Used for messages with maps or photos"""

    await call.message.delete()
