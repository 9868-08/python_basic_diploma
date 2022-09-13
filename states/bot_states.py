from aiogram.dispatcher.filters.state import StatesGroup, State


class SelectCity(StatesGroup):
    wait_city_name = State()
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
    wait_min_price = State()
    wait_max_price = State()

    select_distance_range = State()
    wait_min_distance = State()
    wait_max_distance = State()


class Favorite(StatesGroup):
    show_favorite_hotels = State()


class History(StatesGroup):
    show_history = State()
