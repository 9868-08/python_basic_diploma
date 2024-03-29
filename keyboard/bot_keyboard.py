from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot
import ast


def makekeyboard(location_dict):
    markup = types.InlineKeyboardMarkup()
    for key, value in location_dict.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data=key))
    return markup


def city_markup(cities):
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(
            InlineKeyboardButton(text=city['region_name'],
                                 callback_data=city['id']
                                 )
        )
    return destinations


# @bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith("['value'"):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(
            f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valuefromcallback = ast.literal_eval(call.data)[1]
        keyfromcallback = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text="You Clicked " + valuefromcallback + " and key is " + keyfromcallback)

    if call.data.startswith("['key'"):
        keyfromcallback = ast.literal_eval(call.data)[1]
        # del stringList[keyfromcallback]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of stringList",
                              message_id=call.message.message_id,
                              reply_markup=makekeyboard(),
                              parse_mode='HTML')
