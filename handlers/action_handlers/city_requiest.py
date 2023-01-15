import telebot # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States

# States storage
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage() # you can init here another storage

from loader import bot

# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    city = State() # creating instances of State class is enough from now
    date = State()
    age = State()
    result = State()




@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a city')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    print('bot.get_state(message)', bot.get_state(message))
 

# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)
    print('bot.get_state(message)', bot.get_state(message))


@bot.message_handler(state=MyStates.city)
def date_get(message):
    """
    State 1. Will process when user's state is MyStates.city.
    """
    bot.send_message(message.chat.id, 'Now write me a date')
    bot.set_state(message.from_user.id, MyStates.date, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    print('bot.get_state(message)', bot.get_state(message))
 

# result
@bot.message_handler(state=MyStates.date)
def set_date(message):
    bot.set_state(message.from_user.id, MyStates.result, message.chat.id)
    print(MyStates)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['date'] = message.text
    print('bot.get_state(message)', bot.get_state(message))

@bot.message_handler(state=MyStates.result)
def ready_for_answer(message):
    print ("ready_for_answer(message):")
    msg = ("Ready, take a look:\n<b>"
           f"City: {data['city']}\n"
            f"Date: {data['date']}\n")
    bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)
    print('bot.get_state(message)', bot.get_state(message))


# register filters

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

print("city_requiest.py")
