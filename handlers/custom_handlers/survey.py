from telebot.types import Message
from loader import bot
from states.destination_information import Travel


@bot.message_handler(command=['survey'])
def survey(message: Message):
    bot.set_state(message.from_user.id, Travel, message.chat.id)
    bot.send_message(message, from_user_id, f" Введите город")


@bot.message_handler(state=Travel.city)
def survey(message: Message):
    if message.text.isalpha():
        bot.send_message(f'будем искать отели в городе {message.text}\nзаписал')
        bot.set_state(message.from_user_id, Travel.city, message.chat.id)

        with bot.retrieve_data(message.from_user_id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Имя города должно содержать только буквы')

