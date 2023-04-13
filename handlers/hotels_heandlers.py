from loader import bot
from states import bot_states
from database import diploma_database
import jsonpickle
import json
from datetime import date
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# from handlers.work_with_hotels_handlers.city_handlers import select_city
import time


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def location(call_button):
    calendar, step = create_calendar(call_button)
    bot.send_message(..., f"Укажите {step} заезда", reply_markup=calendar)
    bot.set_state(message.from_user.id, bot_states.MyStates.check_in, message.chat.id)

def start_highprice(message):
    message_dict = json.loads(jsonpickle.encode(message))
    data = dict()
    data['selected_command'] = message_dict['text']
    print(data['selected_command'])
    bot.send_message(message.chat.id, data['selected_command'] + ' was selected. \n Hi, write me a city')

    diploma_database.Hotel_search('highprice')
    request = diploma_database.Hotel_search
    data['city'] = "Boston"
    data['how_much_hotels'] = 2
    data['need_photos'] = "Y"
    data['how_much_photos'] = 2

    bot.set_state(message.from_user.id, bot_states.MyStates.city, message.chat.id)
    return

ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'} #чтобы русифицировать сообщения

def create_calendar(callback_data, min_date=None, is_process=None, locale='ru'):
    if min_date is None:
        min_date = date.today()

    if is_process:
        result, keyboard, step = DetailedTelegramCalendar(min_date=min_date, locale=locale).process(call_data=callback_data.data)
        return result, keyboard, ALL_STEPS[step]
    else:
        calendar, step = DetailedTelegramCalendar(current_date=min_date,
                                         min_date=min_date,
                                         locale=locale).build()
        return calendar, ALL_STEPS[step]