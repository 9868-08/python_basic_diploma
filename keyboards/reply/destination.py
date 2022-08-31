from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_destination():
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton"правим город и дату заезда/выезда")
    return keyboard