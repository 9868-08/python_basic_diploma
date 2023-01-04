from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from config_data import config
from states import bot_states

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)


@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, bot_states.MyStates.far_away_from_center, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a target city')


@bot.message_handler(state=bot_states.MyStates.far_away_from_center)
def name_get(message):
    bot.send_message(message.chat.id, 'How far away from center?')
    bot.delete_state(message.from_user.id, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)

# register filters


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)
