from telebot.handler_backends import State, StatesGroup #States
# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    city = State()  # creating instances of State class is enough from now
    far_away_from_center = State()