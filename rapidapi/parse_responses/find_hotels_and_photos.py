from rapidapi.rapidapi_requests.hotels_request import get_hotel_photos_json
from .hotel_details_utils import distance_str_to_float_in_km, generate_address, trying_to_get_link
from .get_results import get_hotels_dict, get_bestdeal_hotels_dict, trying_to_get_bestdeal_results, \
    trying_to_get_results

from utils.named_tuples import HotelInfo, ID, KM, Link, USD
from typing import Union
from datetime import date

from exceptions.rapidapi_exceptions import ResponseIsEmptyError, BadRapidapiResultError, \
    HotelsNotFoundError


#async def get_hotels_info(data: dict, page: int) -> Union[list[HotelInfo], dict]:
async def get_hotels_info(data: dict, page: int):
    """Gets requiered info for request from state data. Calls parse hotels function"""

    command = data.get('command_type')
    if command == 'bestdeal':
        hotels_dict = await get_bestdeal_hotels_dict(data=data, page=page)
    else:
        hotels_dict = await get_hotels_dict(command=command, data=data, page=page)
    if hotels_dict.get('error') is not None:
        return hotels_dict

    try:
        date_in, date_out = data.get('date_in'), data.get('date_out')

        if command == 'bestdeal':
            results = trying_to_get_bestdeal_results(hotels=hotels_dict, max_distance=data.get('max_distance'))
        else:
            results = trying_to_get_results(hotels=hotels_dict)

        return parse_hotels_info(results=results, date_in=date_in, date_out=date_out)

    except HotelsNotFoundError:
        return {'error': 'hotels_not_found'}
    except BadRapidapiResultError:
        return {'error': 'bad_result'}


#def parse_hotels_info(results: list[dict], date_in: date, date_out: date) -> list[HotelInfo]:
def parse_hotels_info(results: list[dict], date_in: date, date_out: date):
    """Parses found info about each hotel. Returns list of information about each hotel"""

    hotels_info = list()
    for result in results:
        name: str = result.get('name')
        stars: int = int(result.get('starRating'))
        address_info = result.get('address')
        address: str = generate_address(info=address_info)

        hotel_id: ID = result.get('id')
        high_resolution_link: Link = trying_to_get_link(result)

        distance_to_center = result.get('landmarks')[0].get('distance')
        correct_distance: KM = distance_str_to_float_in_km(str_distance=distance_to_center)

        days_in = (date_out - date_in).days
        price_by_night: USD = result.get('ratePlan').get('price').get('exactCurrent')
        total_price: USD = days_in * price_by_night

        coordinates = (result.get('coordinate').get('lat'), result.get('coordinate').get('lon'))

        hotels_info.append(HotelInfo(
            hotel_id=hotel_id,
            name=name,
            stars=stars,
            address=address,
            distance_from_center=correct_distance,
            total_cost=round(total_price, 2),
            cost_by_night=round(price_by_night, 2),
            photo=high_resolution_link,
            coordinates=coordinates
        ))

    return hotels_info


async def get_hotel_photo_links(hotel_id: ID) -> Union[list[Link], dict]:
    """Gets list of hotel photo urls by id"""

    try:
        hotel_photos_json: dict = await get_hotel_photos_json(hotel_id)

    except ResponseIsEmptyError:
        return {'error': 'empty'}

    if hotel_photos_json.get('error') is not None:
        return hotel_photos_json

    hotel_images = hotel_photos_json.get('hotelImages')

    if hotel_images is not None:
        photo_links = [info.get('baseUrl').replace('{size}', 'y') for info in hotel_images]
        return photo_links

    return []
