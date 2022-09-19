from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def create_cities_markup(cities_dict: dict) -> InlineKeyboardMarkup:
    """Creates cities keyboard from dict with info about cities"""

    cities_markup = InlineKeyboardMarkup()
    city_index = 1
    for city_name, city_id in cities_dict.items():
        city_button = InlineKeyboardButton(text=f'{city_index}. {city_name}', callback_data=f'search_in_city{city_id}')
        cities_markup.row(city_button)
        city_index += 1

    return cities_markup
