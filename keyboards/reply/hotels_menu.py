from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def home_menu_keyboard() -> ReplyKeyboardMarkup:
    """Creates basic home menu Keyboard"""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    help_button = KeyboardButton('ℹ️ Справка')
    lopwrice_button = KeyboardButton('⬇️ Недорогие отели')
    highprice_button = KeyboardButton('⬆️ Дорогие отели')
    bestdeal_button = KeyboardButton('🔍 Поиск с параметрами')
    history_button = KeyboardButton('📁 История поиска')
    favorites_button = KeyboardButton('⭐️ Избранное')

    keyboard.row(help_button)
    keyboard.row(lopwrice_button, highprice_button)
    keyboard.row(bestdeal_button)
    keyboard.row(history_button, favorites_button)

    return keyboard


def show_more_hotels_keyboard() -> ReplyKeyboardMarkup:
    """Creates reply markup keyboard that shows with hotels"""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    show_more_button = KeyboardButton('➕ Показать еще')
    go_home_button = KeyboardButton('🏠 Главное меню')
    keyboard.add(show_more_button, go_home_button)

    return keyboard
