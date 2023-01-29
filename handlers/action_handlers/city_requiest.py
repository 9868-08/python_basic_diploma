import telebot  # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States

# States storage
from telebot.storage import StateMemoryStorage

# Now, you can pass storage to bot.
state_storage = StateMemoryStorage()  # you can init here another storage

# bot = telebot.TeleBot("TOKEN", state_storage=state_storage)
from loader import bot


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    city = State()  # creating instances of State class is enough from now
    how_much_hotels = State()
    need_photo = State()
    print_results = State()


@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a city')


# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)



@bot.message_handler(state=MyStates.city)
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.how_much_hotels, message.chat.id)
    bot.send_message(message.chat.id, 'Now write how much hotels to search')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(state=MyStates.how_much_hotels)
def name_get(message):
    """
    State 1. Will process when user's state is MyStates.city.
    """
    bot.send_message(message.chat.id, 'Need photos?')
    bot.set_state(message.from_user.id, MyStates.need_photo, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how_much_hotels'] = message.text


@bot.message_handler(state=MyStates.need_photo)
def ask_age(message):
    bot.send_message(message.chat.id, "Need photo?")
    bot.set_state(message.from_user.id, MyStates.print_results, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['need_photo'] = message.text


@bot.message_handler(state=MyStates.print_results)
def ready_for_answer(message):
    """
    State 3. Will process when user's state is MyStates.need_photo.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"City: {data['city']}\n"
               f"how_much_hotels: {data['how_much_hotels']}\n"
               f"need_photo: {message.text}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)


# register filters

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)
