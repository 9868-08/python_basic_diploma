import telebot # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States

# States storage
from telebot.storage import StateMemoryStorage


# Now, you can pass storage to bot.
state_storage = StateMemoryStorage() # you can init here another storage

#bot = telebot.TeleBot("TOKEN",state_storage=state_storage)
from loader import bot


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
#    name = State()
    city = State()
#    surname = State()
    how_much_hotels = State()
#    age = State()
    need_photos = State()
    how_much_photos = State()
    price_range = State()         #Диапазон цен
    distance = State()              # Диапазон расстояния, на котором находится отель от центра




@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a city')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(state=MyStates.city)
def name_get(message):
    """
    State 2. Will process when user's state is MyStates.city.
    """
    bot.send_message(message.chat.id, 'Need photos? (1 - Yes, 2 - No)')
    bot.set_state(message.from_user.id, MyStates.need_photos, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['need_photos'] = message.text
 
 
@bot.message_handler(state=MyStates.need_photos)
def ask_age(message):
    """
    State 2. Will process when user's state is MyStates.surname.
    """
    bot.send_message(message.chat.id, "How much photos?")
    bot.set_state(message.from_user.id, MyStates.how_much_photos, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_photos'] = message.text


# result
@bot.message_handler(state="*")
def ready_for_answer(message):
    """
    State 3. Will process when user's state is MyStates.age.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"City: {data['city']}\n"
               f"'Need photos?: {data['need_photos']}\n"
               f"How much photos?: {message.text}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)


# register filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)
