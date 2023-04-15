from loader import bot
from states import bot_states
from database import diploma_database
import jsonpickle
import json
# from handlers.work_with_hotels_handlers.city_handlers import select_city
import time


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_highprice(message):
    message_dict = json.loads(jsonpickle.encode(message))
    data = dict()
    data['selected_command'] = message_dict['text']
    print(data['selected_command'])
    bot.send_message(message.chat.id, data['selected_command'] + ' was selected. \n Hi, write me a city')

    # diploma_database.Hotel_search(data['selected_command'])
    # request = diploma_database.Hotel_search

    data['city'] = "Boston"
    data['how_much_hotels'] = 2
    data['need_photos'] = "Y"
    data['how_much_photos'] = 2

    bot.set_state(message.from_user.id, bot_states.MyStates.city, message.chat.id)
    return
