from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional

from database.history.is_hotels_were_found import is_hotels_were_found


async def generate_history_page_keyboard(user_id: int, command_call_time: str) -> Optional[InlineKeyboardMarkup]:
    """Creates Inline keyboard with history show button if hotels were found by called command """

    is_hotels = await is_hotels_were_found(user_id, command_call_time)
    if not is_hotels:
        return None

    keyboard = InlineKeyboardMarkup()
    show_hotels_button = InlineKeyboardButton('⬇️ Показать найденные отели',
                                              callback_data=f'show_history_page{command_call_time}')

    keyboard.row(show_hotels_button)
    return keyboard


def create_history_page_close_keyboard(command_call_time: str) -> InlineKeyboardMarkup:
    """Creates keyboard with history close button"""

    keyboard = InlineKeyboardMarkup()
    close_hotels_button = InlineKeyboardButton('➖ Скрыть найденные отели',
                                                callback_data=f'close_history_page{command_call_time}')

    keyboard.row(close_hotels_button)
    return keyboard


def create_history_page_show_keyboard(command_call_time: str) -> InlineKeyboardMarkup:
    """Creates keyboard with history show button"""

    keyboard = InlineKeyboardMarkup()
    show_hotels_button = InlineKeyboardButton('⬇️ Показать найденные отели',
                                               callback_data=f'show_history_page{command_call_time}')

    keyboard.row(show_hotels_button)
    return keyboard
