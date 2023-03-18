from loader import bot
from states import bot_states
#from handlers.work_with_hotels_handlers.city_handlers import select_city


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_highprice(message):
    bot.send_message(message.chat.id, 'Hi, write me a city')
    bot.set_state(message.from_user.id, bot_states.MyStates.city, message.chat.id)
    return
