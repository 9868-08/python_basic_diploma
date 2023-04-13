ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'} #чтобы русифицировать сообщения

def create_calendar(callback_data, min_date=None, is_process=None, locale='ru'):
    if min_date is None:
        min_date = date.today()

    if is_process:
        result, keyboard, step = DetailedTelegramCalendar(min_date=min_date, locale=locale).process(call_data=callback_data.data)
        return result, keyboard, ALL_STEPS[step]
    else:
        calendar, step = DetailedTelegramCalendar(current_date=min_date,
                                         min_date=min_date,
                                         locale=locale).build()
        return calendar, ALL_STEPS[step]