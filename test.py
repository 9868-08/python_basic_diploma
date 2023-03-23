from loader import bot
from rapidapi.get_info import api_request


request = api_request( 'locations/v3/search',   {"q": 'Boston', "locale": "ru_RU"}, 'GET')
print(request)
