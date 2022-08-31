from telebot.handler_backends import State, StatesGroup
# город
# дата заезда
# дата выезда


class Travel(StatesGroup):
    city = State()
    checkin = State()
    checkout = State()
