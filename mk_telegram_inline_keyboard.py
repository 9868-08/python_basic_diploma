import telebot
import ast
import time
from telebot import types
from states import bot_states

bot = telebot.TeleBot("5353535107:AAEPSYNZarSnJY1hcQr11WVCPMGxyZp4PgA")

stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
crossIcon = u"\u274C"


def get_location_id(message, location_dict):
    '''location_dict = [{'id': '660', 'region_name': 'Бостон, Suffolk County, Массачусетс, США'},
                     {'id': '6340396', 'region_name': 'Даунтаун-Бостон, Бостон, Массачусетс, США'},
                     {'id': '5459778', 'region_name': 'Бостон, Массачусетс, США (BOS-Логан, международный)'},
                     {'id': '3000448054', 'region_name': 'Бостон, Нью-Йорк, США'}]'''
    # print(location_dict)
    # print(stringList)
    # stringList = location_dict
    bot.send_message(message.chat.id, 'location_dic, location_dict = ' + str(location_dict))
#    print('def get_location_id')
    bot.set_state(message.from_user.id, bot_states.MyStates.city_detail, message.chat.id)


def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
        types.InlineKeyboardButton(text=crossIcon,
                                   callback_data="['key', '" + key + "']"))
        print(key, value)

    return markup


# @bot.message_handler(commands=['test'])
@bot.message_handler(state=bot_states.MyStates.city_detail)
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the values of stringList",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if (call.data.startswith("['value'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del stringList[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of stringList",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),


                              parse_mode='HTML')


# location_dict = [{'id': '660', 'region_name': 'Бостон, Suffolk County, Массачусетс, США'}, {'id': '6340396', 'region_name': 'Даунтаун-Бостон, Бостон, Массачусетс, США'}, {'id': '5459778', 'region_name': 'Бостон, Массачусетс, США (BOS-Логан, международный)'}, {'id': '3000448054', 'region_name': 'Бостон, Нью-Йорк, США'}]
# print(location_dict)
'''while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)'''