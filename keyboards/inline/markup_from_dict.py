from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def inline_markup_from_dict(dictionary: dict) -> InlineKeyboardMarkup:
    """Converts keyboard dict to inline markup"""

    keyboard = InlineKeyboardMarkup()
    keyboard_info: list = dictionary.get('inline_keyboard')
    for row in keyboard_info:
        buttons = list()
        for button in row:
            if button.get('url'):
                buttons.append(InlineKeyboardButton(
                    text=button['text'],
                    url=button['url']
                ))
            else:
                buttons.append(InlineKeyboardButton(
                    text=button['text'],
                    callback_data=button['callback_data']
                ))
        keyboard.row(*buttons)

    return keyboard
