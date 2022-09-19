from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot_pagination import InlineKeyboardPaginator

from keyboards.inline.markup_from_dict import inline_markup_from_dict
from utils.named_tuples import HotelInfo, Degrees


def create_hotel_keyboard(info: HotelInfo) -> InlineKeyboardMarkup:
    """
    Creates hotel keyboard with next buttons:
    - Booking hotel
    - Show on maps
    - Get photos
    - Add to favorites
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    hotel_id = info.hotel_id
    booking_button = InlineKeyboardButton('🌐  Забронировать', url=f'hotels.com/ho{hotel_id}')

    latitude, longitude = info.coordinates
    maps_button = InlineKeyboardButton('📍 На карте', callback_data=f'get_hotel_map{latitude}/{longitude}')

    photos_button = InlineKeyboardButton('📷  Фото', callback_data=f'get_hotel_photos{hotel_id}')

    favorite_button = InlineKeyboardButton('❤️ Добавить в избранное', callback_data='add_to_favorites')

    keyboard.add(booking_button, maps_button, photos_button, favorite_button)
    return keyboard


def edit_hotel_keyboard_by_favorite(current_keyboard: InlineKeyboardMarkup, is_favorite: bool) -> InlineKeyboardMarkup:
    keyboard_dict = dict(current_keyboard)
    favorite_button: dict = keyboard_dict['inline_keyboard'][-1][0]
    if is_favorite:
        favorite_button['text'] = '🤍 Удалить из избранного'
        favorite_button['callback_data'] = 'delete_from_favorites'
    else:
        favorite_button['text'] = '❤️ Добавить в избранное'
        favorite_button['callback_data'] = 'add_to_favorites'

    return inline_markup_from_dict(dictionary=keyboard_dict)


def create_map_keyboard(latitude: Degrees, longitude: Degrees) -> InlineKeyboardMarkup:
    """
    Creates map keyboard with next buttons:
    - Show in Google Maps
    - Show in Yandex Maps
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    gmaps_link = f'http://maps.google.com/maps?q={latitude},{longitude}'
    ymaps_link = f'http://maps.yandex.ru/?text={latitude},{longitude}'

    google_maps_button = InlineKeyboardButton(text='Открыть в Google Maps', url=gmaps_link)
    yandex_maps_button = InlineKeyboardButton(text='Открыть в Яндекс Картах', url=ymaps_link)
    close_message_button = InlineKeyboardButton(text='➖ Закрыть', callback_data='close_message')

    keyboard.add(google_maps_button, yandex_maps_button, close_message_button)

    return keyboard


def create_photos_keyboard(photos_amount: int, page: int = 1) -> InlineKeyboardMarkup:
    """Creates keyboard of paginator by current page"""

    paginator = InlineKeyboardPaginator(photos_amount, current_page=page, data_pattern='get_photo{page}')
    paginator.add_after(InlineKeyboardButton(text='➖ Закрыть', callback_data='close_message'))

    return paginator.markup
