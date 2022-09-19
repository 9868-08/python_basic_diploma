from exceptions.rapidapi_exceptions import ResponseIsEmptyError
from rapidapi.rapidapi_requests.cities_request import get_cities_json


async def find_cities(city: str) -> dict:
    """
    Parses json response to get cities dict.
    Returns dict where keys are cities names and values are cities id
    """

    cities_dict: dict = await trying_to_get_cities_dict(city=city)

    if cities_dict.get('error') is not None:
        return cities_dict

    city_suggestions: list = cities_dict.get('suggestions')
    city_entities: list = city_suggestions[0]['entities']
    if not city_entities:
        return {'error': 'cities_not_found'}

    cities_with_id = dict()
    for city_dict in city_entities:
        name, city_id = city_dict.get('name'), city_dict.get('destinationId')
        cities_with_id[name] = city_id

    return cities_with_id


async def trying_to_get_cities_dict(city: str) -> dict:
    """Tries to get dict with cities 3 times if result not found returns dict with error"""

    attempts = 0
    while attempts < 3:
        try:
            cities_dict: dict = await get_cities_json(city=city)
            attempts += 1
            if isinstance(cities_dict, dict):
                return cities_dict
        except ResponseIsEmptyError:
            return {'error': 'empty'}

    return {'error': 'empty'}
