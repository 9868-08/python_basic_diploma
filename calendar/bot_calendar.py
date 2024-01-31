from telegram_bot_calendar import DetailedTelegramCalendar

from states.bot_states import MyStates
from loader import bot

ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}  # чтобы русифицировать сообщения

# Создадим функцию генерирующую календарь
def create_calendar(callback_data, min_date=None, is_process=None, locale='ru'):
    if min_date is None:
        min_date = date.today()

    if is_process:
        result, keyboard, step = DetailedTelegramCalendar(min_date=min_date, locale=locale).process(
            call_data=callback_data.data)
        return result, keyboard, ALL_STEPS[step]
    else:
        calendar, step = DetailedTelegramCalendar(current_date=min_date,
                                                  min_date=min_date,
                                                  locale=locale).build()
        return calendar, ALL_STEPS[step]


# Отправляем его
@bot.callback_query_handler(func=None, state=MyStates.city)  # Допустим пользователь выбирал город через кнопки
def location(call_button):
    calendar, step = create_calendar(call_button)
    bot.send_message(..., f"Укажите {step} заезда", reply_markup=calendar)


# Ловим состояние выбора даты
@bot.callback_query_handler(func=None, state=MyStates.check_in)
def select_check_in(call_button):
    result, keyboard, step = create_calendar(call_button, is_process=True)

    if not result and keyboard:
        # Продолжаем отсылать шаги, пока не выберут дату "result"
        bot.edit_message_text(f'Укажите {step} заезда',
                              call_button.from_user.id,
                              call_button.message.message_id,
                              reply_markup=keyboard)

    elif result:
        # Дата выбрана, сохраняем и создаем новый календарь с датой отъезда
        calendar, step = create_calendar(call_button, min_date=result)


if __name__ == '__main__':
    # set_default_commands(bot)
    bot.infinity_polling(skip_pending=True)