from telebot import TeleBot
from datetime import date
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loader import bot
from states import bot_states


@bot.message_handler(state=bot_states.MyStates.check_in)
def start(m):
    calendar, step = DetailedTelegramCalendar(max_date=date.today()).build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar(max_date=date.today()).process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)


