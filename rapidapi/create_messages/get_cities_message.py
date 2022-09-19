from typing import Union
from utils.named_tuples import CitiesMessage

from rapidapi.parse_responses.find_cities import find_cities

from keyboards.inline.city_keyboard.cities_keyboard import create_cities_markup


async def create_cities_message(city: str) -> Union[CitiesMessage, dict]:
    """Creates message of found cities. Returns message text and inline buttons with cities"""

    found = await find_cities(city=city)

    if found.get('error') is not None:
        return found

    if len(found) == 1:
        text = f'<b>Искать в городе {"".join(city for city in found)}?</b>'
    else:
        text = '↘️ <b>Пожалуйста, уточните город</b>'

    buttons = create_cities_markup(cities_dict=found)
    return CitiesMessage(message=text, buttons=buttons)
