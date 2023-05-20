# import telebot
# import ast
import time
from telebot import types
from states import bot_states
# from uuid import uuid4

# bot = telebot.TeleBot("5353535107:AAEPSYNZarSnJY1hcQr11WVCPMGxyZp4PgA")

# stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}

# crossIcon = u"\u274C"
from loader import bot


def get_location_id(message, location_dict):
    # print(location_dict)
    # print(stringList)
    # stringList = location_dict
    bot.send_message(message.chat.id, 'location_dic, location_dict = ' + str(location_dict))
    #    print('def get_location_id')
    bot.set_state(message.from_user.id, bot_states.MyStates.city_detail, message.chat.id)


def makeKeyboard(message, location_dict):
    markup = types.InlineKeyboardMarkup()
#    stringList = location_dict

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     stringList = message.text

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
def handle_command_adminwindow(message, location_dict):
    bot.send_message(chat_id=message.chat.id,
                     text="Where are some locations. Select correct please: ",
                     reply_markup=makeKeyboard(message, location_dict),
                     parse_mode='HTML')


# location_dict = [{'id': '660', 'region_name': 'Бостон, Suffolk County, Массачусетс, США'}, {'id': '6340396', 'region_name': 'Даунтаун-Бостон, Бостон, Массачусетс, США'}, {'id': '5459778', 'region_name': 'Бостон, Массачусетс, США (BOS-Логан, международный)'}, {'id': '3000448054', 'region_name': 'Бостон, Нью-Йорк, США'}]
# print(location_dict)
'''while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)'''
