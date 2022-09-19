from aiohttp import ClientSession, ClientTimeout, ServerTimeoutError
from asyncio.exceptions import TimeoutError

from config_data.work_with_rapidapi_keys import get_headers_by_correct_rapidapi_key, change_rapid_api_key


async def request_to_api(url: str, querystring: dict) -> dict:
    """Basic function that sends request to rapidapi with aiohttp methods"""

    timeout = ClientTimeout(total=10)
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.get(url=url,
                                   headers=get_headers_by_correct_rapidapi_key(),
                                   params=querystring) as response:
                if response.ok:
                    response_json = await response.json()

                    return response_json

                if response.status == 429:
                    change_rapid_api_key()

    except ServerTimeoutError:
        return {'error': 'timeout'}
    except TimeoutError:
        return {'error': 'timeout'}
