from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def create_history_menu():
    """Creates reply keyboard when user history is shows"""

    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    clear_history_button = KeyboardButton('❌ Очистить историю')
    go_home_button = KeyboardButton('🏠 Главное меню')

    keyboard.add(clear_history_button, go_home_button)
    return keyboard
