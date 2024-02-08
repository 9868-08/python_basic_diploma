from telebot.handler_backends import State, StatesGroup  # States


# состояния класса
class MyStates(StatesGroup):
    city = State()
    how_much_hotels = State()
    need_photos = State()
    how_much_photos = State()
    far_away_from_center = State()
    print_results = State()
    rapidapi_get_cityid = State()
    hotel_id_list = State()
    check_in = State()
    check_out = State()
    city_detail = State()
    location_confirmation = State()
    bestdeal = State()
    bestdeal_print_results = State()
    bestdeal_distance_min_flag = State()
    bestdeal_distance_max_flag = State()
