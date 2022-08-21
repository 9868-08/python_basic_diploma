from aiogram.dispatcher.filters.state import StatesGroup, State


class SelectCity(StatesGroup):
    city_name = State()
    select_city = State()


class SelectDates(StatesGroup):
    start_select_date_in = State()
    select_date_in = State()

    start_select_date_out = State()
    select_date_out = State()

    is_date_correct = State()


class GetHotels(StatesGroup):
    is_info_correct = State()
    get_hotels_menu = State()


class BestDeal(StatesGroup):
    select_price_range = State()
    min_price = State()
    max_price = State()

    select_distance_range = State()
    min_distance = State()
    max_distance = State()


class Favorite(StatesGroup):
    show_favorite_hotels = State()


class History(StatesGroup):
    show_history = State()
