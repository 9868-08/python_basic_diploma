from rapidapi.rapidapi_requests.hotels_request import get_hotels_json, get_bestdeal_hotels_json
from .hotel_details_utils import distance_str_to_float_in_km

from exceptions.rapidapi_exceptions import BadRapidapiResultError, ResponseIsEmptyError, HotelsNotFoundError
from utils.named_tuples import KM


async def get_hotels_dict(command: str, data: dict, page: int) -> dict:
    """Gets hotels dict from rapidapi"""

    sort_by = 'PRICE' if command == 'lowprice' else 'PRICE_HIGHEST_FIRST'
    date_in, date_out = data.get('date_in'), data.get('date_out')

    try:
        hotels_dict: dict = await get_hotels_json(destination_id=data.get('city_id'),
                                                  date_in=date_in, date_out=date_out,
                                                  sort_by=sort_by, page=page)
        return hotels_dict

    except ResponseIsEmptyError:
        return {'error': 'empty'}


async def get_bestdeal_hotels_dict(data: dict, page: int):
    """Gets hotels dictionary from rapidapi with user parametrs in request"""

    min_price, max_price = data.get('min_price'), data.get('max_price')
    date_in, date_out = data.get('date_in'), data.get('date_out')

    try:
        hotels_dict_with_min_distance = await get_bestdeal_hotels_json(destination_id=data.get('city_id'),
                                                                       date_in=date_in, date_out=date_out, page=page,
                                                                       min_price=min_price, max_price=max_price)
        return hotels_dict_with_min_distance
    except ResponseIsEmptyError:
        return {'error': 'empty'}


def trying_to_get_results(hotels: dict) -> list:
    """Tries to get results from dictionary with hotels info"""

    if hotels.get('result') == 'OK':
        search_results: dict = hotels.get('data').get('body').get('searchResults')

        results: list = search_results.get('results')
        return results

    raise BadRapidapiResultError


def trying_to_get_bestdeal_results(hotels: dict, max_distance: int) -> list:
    """Tries to get results that from dictionary with info about matching hotels"""

    results = trying_to_get_results(hotels=hotels)
    return slice_hotels_results_by_max(results=results, max_distance=max_distance)


def slice_hotels_results_by_max(results: list, max_distance: int):
    """Slices hotels properties up to hotel with maximum distance"""

    index = len(results) - 1
    while index >= 0:
        hotel = results[index]
        distance_to_center = hotel.get('landmarks')[0].get('distance')
        distance: KM = distance_str_to_float_in_km(str_distance=distance_to_center)
        if distance <= max_distance:
            break
        index -= 1

    if len(results[:index + 1]) == 0:
        raise HotelsNotFoundError

    return results[:index + 1]
