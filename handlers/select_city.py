from states import bot_states
from telebot.storage import StateMemoryStorage
from loader import bot
import test
import rapidapi.get_info
import mk_telegram_inline_keyboard

state_storage = StateMemoryStorage()


@bot.message_handler(state=bot_states.MyStates.city)
def MyStates_city(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text

    location_dict = rapidapi.get_info.api_request('locations/v3/search', {"q": data['city'], "locale": "ru_RU"},
                                                  'GET')  # предоставляет ответ по выбранной локации из которого нужно вытянуть id локации
    #    location_id = location_json['sr'][0]['gaiaId']
#    bot.send_message(message.chat.id, " location_dict = " + str(location_dict))

    bot.set_state(message.from_user.id, bot_states.MyStates.how_much_hotels, message.chat.id)
    bot.send_message(message.chat.id, 'Now write how much hotels to search')
    return


@bot.message_handler(state=bot_states.MyStates.how_much_hotels)
def MyStates_how_much_hotels(message):
    bot.send_message(message.chat.id, 'Need photos?')
    bot.set_state(message.from_user.id, bot_states.MyStates.need_photos, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_hotels'] = message.text


@bot.message_handler(state=bot_states.MyStates.need_photos)
def MyStates_need_photos(message):
    if message.text == "Y":
        bot.send_message(message.chat.id, 'How much photos?')
        bot.set_state(message.from_user.id, bot_states.MyStates.print_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text
    else:
        bot.send_message(message.chat.id, 'ok - no photos')
        bot.set_state(message.from_user.id, bot_states.MyStates.print_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text
            data['need_photos'] = "N"
            data['how_much_photos'] = 0


@bot.message_handler(state=bot_states.MyStates.print_results)
def print_results(message):
    data = dict()
    data['city'] = "Boston"
    data['how_much_hotels'] = 2
    data['need_photos'] = "Y"
    data['how_much_photos'] = 2

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_photos'] = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"City: {data['city']}\n"
               f"how_much_hotels: {data['how_much_hotels']}\n"
               f"need photos: {data['need_photos']}\n"
               f"how_much_photos: {message.text}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)

    # предоставляет ответ по выбранной локации из которого нужно вытянуть id локации
    location_dict = rapidapi.get_info.api_request('locations/v3/search', {"q": 'Boston', "locale": "ru_RU"}, 'GET')
#    location_id = location_json['sr'][0]['gaiaId']
    location_id = mk_telegram_inline_keyboard.get_location_id(message, location_dict)
#    location_id = mk_telegram_inline_keyboard.get_location_id(location_dict)
    #    hotel_id_json = def_hotel_id(location_id)

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": location_id},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 150,
            "min": 100
        }}
    }

    hotel_id_json = rapidapi.get_info.api_request('properties/v2/list', payload, 'POST')
    parsed = hotel_id_json['data']['propertySearch']
    hotel_id_list = []
    # import pprint
    count = 0
    for item in parsed['properties']:
        # print (count, int(data['how_much_photos']))
        if count + 1 > int(data['how_much_hotels']):
            break
        hotel_id = int(item['id'])
        payload = {"currency": "USD", "eapid": 1, "locale": "en_US", "siteId": 300000001, "propertyId": hotel_id}
        hotel_id_list.append(hotel_id)
        print(item['name'])
        #    pprint.pprint(item)
        bot.send_message(message.chat.id, 'найден отель = ' + item['name'])
        # bot.send_photo(str(item['propertyImage']['image']['url']))
        bot.send_photo(message.chat.id, str(item['propertyImage']['image']['url']), caption='фото в отеле '+ item['name'])
        count += 1
    return hotel_id_list
