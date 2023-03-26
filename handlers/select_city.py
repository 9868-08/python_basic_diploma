import rapidapi.get_info
from states import bot_states
from telebot.storage import StateMemoryStorage
from loader import bot
from rapidapi import get_info
state_storage = StateMemoryStorage()


@bot.message_handler(state=bot_states.MyStates.city)
def start_ex(message):
    bot.set_state(message.from_user.id, bot_states.MyStates.how_much_hotels, message.chat.id)
    bot.send_message(message.chat.id, 'Now write how much hotels to search')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(state=bot_states.MyStates.how_much_hotels)
def name_get(message):
    bot.send_message(message.chat.id, 'Need photos?')
    bot.set_state(message.from_user.id, bot_states.MyStates.need_photos, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_hotels'] = message.text


@bot.message_handler(state=bot_states.MyStates.need_photos)
def name_get(message):
    if message.text == "Y":
        bot.send_message(message.chat.id, 'How much photos?')
        bot.set_state(message.from_user.id, bot_states.MyStates.print_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photos'] = message.text
    else:
        bot.send_message(message.chat.id, 'ok - no photos')
        bot.set_state(message.from_user.id, bot_states.MyStates.print_results, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['how_much_photos'] = 0


@bot.message_handler(state=bot_states.MyStates.print_results)
def ready_for_answer(message):
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

#    hotel_id_list = rapidapi.get_info.def_rapidapy_start(data['city'])
    hotel_id_list = rapidapi.get_info.api_request('locations/v3/search', {"q": 'Boston', "locale": "ru_RU"}, 'GET')
    print('hotel_id_list type=', type(hotel_id_list))
    print('hotel_id_list=', hotel_id_list)
    for hotel in hotel_id_list:
        count = 0
        while count <= int(data['how_much_hotels']):
            hotel_info = rapidapi.get_info.def_hotel_detail(hotel)
            bot.send_message(message.chat.id, 'count='+str(count)+' hotel='+str(hotel), parse_mode="html")
            bot.send_message(message.chat.id, hotel_info['data']['propertyInfo']['summary']['name'], parse_mode="html")
            count += 1
#            print(hotel_info)

