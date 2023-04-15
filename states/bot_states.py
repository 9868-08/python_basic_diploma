from telebot import State
from telebot.handler_backends import State, StatesGroup  # States


class MyStates(StatesGroup):
    city = State()
    how_much_hotels = State()
    need_photos = State()
    how_much_photos = State()
    far_away_from_center = State()
    print_results = State()
    rapidapi_get_cityid = State()
    hotel_id_list = State()


class SelectDates(StatesGroup):
    start_select_date_in = State()
    select_date_in = State()
