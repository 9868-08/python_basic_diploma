from aiogram.dispatcher.filters import Command, Text
from aiogram.types.callback_query import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from database.history.get_history import get_history, get_found_hotels_of_command
from database.history.delete_history import clear_history
from database.history.sended_history_messages import SendedHistory
from database.utils.utils import get_correct_hotel_info_by_favorites

from keyboards.reply.history_menu import create_history_menu
from keyboards.inline.history_keyboard.history_page_keyboard import generate_history_page_keyboard, \
     create_history_page_close_keyboard, create_history_page_show_keyboard
from states.bot_states import History
from photos.work_with_photos import Photos

from utils.work_with_messages.send_message_with_photo import trying_to_send_with_photo
from utils.misc.work_with_errors import finish_with_error
from utils.named_tuples import HistoryPage, HotelMessage
from loader import dp


@dp.message_handler(Command('history'), state='*')
async def show_history(message: Message, state: FSMContext):
    """Sends the user his history"""

    await History.show_history.set()

    user_history: list[HistoryPage] = await get_history(message=message)
    if not user_history:
        await finish_with_error(message=message, state=state, error='history_empty')
        return

    history_to_delete: SendedHistory = await send_history_pages(message, user_history)
    await state.update_data(history_to_delete=history_to_delete)


@dp.message_handler(Text('📁 История поиска'), state='*')
async def show_history_(message: Message, state: FSMContext):
    await show_history(message=message, state=state)


async def send_history_pages(message: Message, history: list[HistoryPage]) -> SendedHistory:
    """Sends history pages to user"""

    history_caption = await message.bot.send_photo(photo=Photos.history.value, chat_id=message.chat.id,
                                                   caption='<b>История поиска:</b>', reply_markup=create_history_menu())
    sended_history = SendedHistory(history_caption=history_caption)
    for history_page in history:
        keyboard = await generate_history_page_keyboard(user_id=message.chat.id,
                                                        command_call_time=history_page.command_call_time)
        command_call_info = await message.answer(text=history_page.text, reply_markup=keyboard)
        sended_history.add_new_command_message(command_call_info)

    return sended_history


@dp.callback_query_handler(lambda call: call.data.startswith('show_history_page'), state=History.show_history)
async def show_hotels_of_command(call: CallbackQuery, state: FSMContext):
    """Sends the user hotels from selected history page"""

    command_call_time = call.data.lstrip('show_history_page')

    await call.message.edit_reply_markup(create_history_page_close_keyboard(command_call_time))
    found_hotels: list[HotelMessage] = await get_found_hotels_of_command(user_id=call.message.chat.id,
                                                                         call_time=command_call_time)

    state_data = await state.get_data()
    sended_history_messages: SendedHistory = state_data.get('history_to_delete')

    for hotel_message in found_hotels:
        hotel_message = await get_correct_hotel_info_by_favorites(user_id=call.message.chat.id, hotel=hotel_message)
        message_with_hotel = await trying_to_send_with_photo(message_from_user=call.message,
                                                             hotel_message=hotel_message)
        sended_history_messages.add_new_found_hotel(command_cal_time=command_call_time, hotel=message_with_hotel)

    await state.update_data(history_to_delete=sended_history_messages)


@dp.callback_query_handler(lambda call: call.data.startswith('close_history_page'), state=History.show_history)
async def close_hotels_of_command(call: CallbackQuery, state: FSMContext):
    """Deletes hotels messages from selected history page"""

    command_call_time = call.data.lstrip('close_history_page')

    await call.message.edit_reply_markup(create_history_page_show_keyboard(command_call_time=command_call_time))

    state_data = await state.get_data()
    sended_history_messages: SendedHistory = state_data.get('history_to_delete')

    await sended_history_messages.hide_found_hotels(command_cal_time=command_call_time)
    await state.update_data(history_to_delete=sended_history_messages)


@dp.message_handler(Text('❌ Очистить историю'), state=History.show_history)
async def clear_user_history(message: Message, state: FSMContext):
    """Clear all user history"""

    state_data = await state.get_data()
    history_to_delete: SendedHistory = state_data.get('history_to_delete')

    await clear_history(user_id=message.chat.id)
    await history_to_delete.delete_all_history_messages()

    await finish_with_error(message=message, state=state, error='history_empty')
