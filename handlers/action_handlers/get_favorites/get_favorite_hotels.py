from aiogram.types.callback_query import CallbackQuery, Message
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from database.favorites.get_favorites import get_favorite_hotels
from database.favorites.add_favorite import add_to_favorites
from database.favorites.delete_from_favorites import delete_from_favorites
from database.favorites.delete_favorites import clear_favorites
from database.utils.utils import is_favorites_are_over

from states.bot_states import Favorite
from photos.work_with_photos import Photos
from keyboards.inline.hotel_keyboards.hotel_keyboard import edit_hotel_keyboard_by_favorite
from keyboards.reply.favorite_hotels_menu import create_favorites_menu
from utils.named_tuples import HotelMessage
from utils.misc.work_with_errors import finish_with_error
from utils.work_with_messages.send_message_with_photo import trying_to_send_with_photo
from loader import dp


@dp.message_handler(Command('favorites'), state='*')
async def show_favorite_hotels(message: Message, state: FSMContext):
    """Sends the user his favorite hotels"""

    await Favorite.show_favorite_hotels.set()
    sended_messages = list()

    favorite_hotels: list[HotelMessage] = await get_favorite_hotels(message=message)
    if favorite_hotels:
        to_delete = await message.bot.send_photo(photo=Photos.favorites.value, chat_id=message.chat.id,
                                                 caption='<b>Избранные отели:</b>',
                                                 reply_markup=create_favorites_menu())
        sended_messages.append(to_delete)
        await state.update_data(favorite_message_to_delete=to_delete)
    else:
        await finish_with_error(message=message, error='favorites_empty', state=state)
        return

    for hotel in favorite_hotels:
        sended_hotel = await trying_to_send_with_photo(message_from_user=message, hotel_message=hotel)
        sended_messages.append(sended_hotel)

    await state.update_data(favorites_to_delete=sended_messages)


@dp.message_handler(Text('⭐️ Избранное'), state='*')
async def show_favorite_hotels_(message: Message, state: FSMContext):
    await show_favorite_hotels(message=message, state=state)


@dp.callback_query_handler(lambda call: call.data == 'add_to_favorites', state='*')
async def add_hotel_to_favorites(call: CallbackQuery):
    """Adds hotel to favorites by callback"""

    await add_to_favorites(message=call.message)
    await call.answer('Добавлено в избранное!', show_alert=False)
    await call.message.edit_reply_markup(edit_hotel_keyboard_by_favorite(current_keyboard=call.message.reply_markup,
                                                                         is_favorite=True))


@dp.callback_query_handler(lambda call: call.data == 'delete_from_favorites', state='*')
async def delete_hotel_from_favorites(call: CallbackQuery, state: FSMContext):
    """Deletes hotel from favorites by callback"""

    await delete_from_favorites(message=call.message)
    await call.answer('Удалено из избранного!', show_alert=False)
    await call.message.edit_reply_markup(edit_hotel_keyboard_by_favorite(current_keyboard=call.message.reply_markup,
                                                                         is_favorite=False))

    current_state = await state.get_state()
    if current_state == Favorite.show_favorite_hotels.state:
        await call.message.delete()

        is_favorites_are_over_ = await is_favorites_are_over(message=call.message)
        if is_favorites_are_over_:
            state_data = await state.get_data()
            message_to_delete: Message = state_data.get('favorite_message_to_delete')
            await finish_with_error(message=call.message, error='favorites_empty', state=state,
                                    to_delete=message_to_delete)


@dp.message_handler(Text('❌ Очистить избранное'), state=Favorite.show_favorite_hotels)
async def clear_favorite_hotels(message: Message, state: FSMContext):
    """Clear all user favorite hotels"""

    state_data = await state.get_data()
    favorites_to_delete: list[Message] = state_data.get('favorites_to_delete')

    await clear_favorites(user_id=message.chat.id)
    for favorite_hotel in favorites_to_delete:
        try:
            await favorite_hotel.delete()
        except MessageToDeleteNotFound:
            continue

    await finish_with_error(message=message, state=state, error='favorites_empty')
