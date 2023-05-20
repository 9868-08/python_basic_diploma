from loader import bot
from states import bot_states
# from database import diploma_database
import json
import jsonpickle
import ast
from telebot import types

# from datetime import date
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# from handlers.work_with_hotels_handlers.city_handlers import select_city
# import time
# from handlers import get_checkin


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_highprice(message):
    message_dict = json.loads(jsonpickle.encode(message))
    data = dict()
    data['selected_command'] = message_dict['text']
    print(data['selected_command'])
    bot.send_message(message.chat.id, data['selected_command'] + ' was selected. \n Hi, write me a city')

    # diploma_database.Hotel_search(data['selected_command'])
    # request = diploma_database.Hotel_search
    bot.set_state(message.from_user.id, bot_states.MyStates.city, message.chat.id)
#    get_checkin.create_calendar(1)
    # create_calendar(callback_data, min_date=None, is_process=None, locale='ru'):
    return


def get_location_id(message, location_dict):
    # print(location_dict)
    # print(location_dict)
    # location_dict = location_dict
    bot.send_message(message.chat.id, 'location_dic, location_dict = ' + str(location_dict))
    #    print('def get_location_id')
    bot.set_state(message.from_user.id, bot_states.MyStates.city_detail, message.chat.id)


def makeKeyboard(message):
    markup = types.InlineKeyboardMarkup()
    location_dict = dict()
    location_dict = {'3000448054': 'Бостон, Нью-Йорк, США', '5459778': 'Бостон, Массачусетс, США (BOS-Логан, международный)',
     '6340396': 'Даунтаун-Бостон, Бостон, Массачусетс, США', '660': 'Бостон, Suffolk County, Массачусетс, США'}

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     location_dict = message.text

#    print(data['city'])
#    location_dict = rapidapi.get_info.api_request('locations/v3/search', {"q": data['city'], "locale": "ru_RU"}, 'GET')
    for key, value in location_dict.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data=key))
        print(key, value)
    print(markup.keyboard)
    return markup


# @bot.message_handler(commands=['test'])
@bot.message_handler(state=bot_states.MyStates.city_detail)
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Where are some locations. Select correct please: ",
                     reply_markup=makeKeyboard(message),
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call, message):
    location_dict = dict()
    if call.data.startswith("['value'"):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(
            f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

    if call.data.startswith("['key'"):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del location_dict[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of location_dict",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(message, location_dict),

                              parse_mode='HTML')
