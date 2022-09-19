from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def price_range_keyboard():
    """Creates inline keyboard for price range selecting"""

    keyboard = InlineKeyboardMarkup(row_width=1)

    min_price_button = InlineKeyboardButton('➖ Указать от скольки', callback_data='select_min_price')
    max_price_button = InlineKeyboardButton('➕ Указать до скольки', callback_data='select_max_price')
    complete_button = InlineKeyboardButton('✅ Готово', callback_data='end_price_range')

    keyboard.add(min_price_button, max_price_button, complete_button)
    return keyboard


def distance_range_keyboard():
    """Creates inline keyboard for distance selecting"""

    keyboard = InlineKeyboardMarkup(row_width=1)

    max_distance_button = InlineKeyboardButton('➕ Указать расстояние', callback_data='select_max_distance')
    complete_button = InlineKeyboardButton('✅ Готово', callback_data='end_distance_range')

    keyboard.add(max_distance_button, complete_button)
    return keyboard
