from rapidapi.rapidapi_requests.requests_to_api import request_to_api

from datetime import date
from utils.named_tuples import ID

from exceptions.rapidapi_exceptions import ResponseIsEmptyError


async def get_hotels_json(destination_id: str, date_in: date, date_out: date, sort_by: str, page: int) -> dict:
    """Sends search request to rapidapi by selected city id. Returns json of found hotels"""
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destination_id, "pageNumber": str(page), "pageSize": "25",
                   "checkIn": str(date_in), "checkOut": str(date_out), "adults1": "1",
                   "sortOrder": sort_by, "locale": "en_US",
                   "currency": "USD", 'landmarkIds': 'City center'}

    hotels_json = await request_to_api(url=url, querystring=querystring)
    if hotels_json is None:
        raise ResponseIsEmptyError

    return hotels_json


async def get_bestdeal_hotels_json(destination_id: str, date_in: date, date_out: date, page: int,
                                   min_price: int, max_price: int) -> dict:
    """Sends search request with user parametrs to rapidapi by selected city id. Returns json of found hotels"""

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destination_id, "pageNumber": str(page), "pageSize": "25",
                   "checkIn": str(date_in), "checkOut": str(date_out), "adults1": "1",
                   "priceMin": str(min_price), "priceMax": str(max_price), "sortOrder": "DISTANCE_FROM_LANDMARK",
                   "locale": "en_US", "currency": "USD", "landmarkIds": "City center"}

    hotels_json = await request_to_api(url=url, querystring=querystring)
    if hotels_json is None:
        raise ResponseIsEmptyError

    return hotels_json


async def get_hotel_photos_json(hotel_id: ID) -> dict:
    """Sends search request to rapidapi by selected hotel id. Returns json of found photos"""

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": str(hotel_id)}

    photos_json = await request_to_api(url=url, querystring=querystring)
    if photos_json is None:
        raise ResponseIsEmptyError
    return photos_json
