from loader import bot
from states import bot_states
from database import diploma_database
#from handlers.work_with_hotels_handlers.city_handlers import select_city
import time


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_highprice(message):
    diploma_database.Hotel_search('highprice')
    request = diploma_database.Hotel_search
    bot.send_message(message.chat.id, 'Hi, write me a city')
    #    bot.set_state(message.from_user.id, bot_states.MyStates.city, message.chat.id)
    data = dict()
    data['city'] = "Boston"
    data['how_much_hotels'] = 2
    data['need_photos'] = "Y"
    data['how_much_photos'] = 2
    print(data)
    bot.set_state(message.from_user.id, bot_states.MyStates.city, message.chat.id)
    return
