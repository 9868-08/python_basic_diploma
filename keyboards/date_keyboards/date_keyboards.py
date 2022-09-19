from telegram_bot_calendar import DetailedTelegramCalendar

from datetime import datetime
from typing import Optional

from utils.named_tuples import CalendarMarkupAndStep

CUSTOM_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}


class CustomCalendar(DetailedTelegramCalendar):
    """
    Calendar keyboard with user-friendly interface
    """

    next_button = '➡️'
    prev_button = '⬅️'

    def __init__(self, min_date=datetime.now().date()):
        super().__init__(locale='ru', min_date=min_date)


def create_calendar(minimal_date: Optional[datetime] = None) -> CalendarMarkupAndStep:
    """Creates a calendar and gets step of input"""

    if minimal_date is None:
        calendar, step = CustomCalendar().build()
    else:
        calendar, step = CustomCalendar(min_date=minimal_date).build()

    return CalendarMarkupAndStep(calendar=calendar, date_type=CUSTOM_STEPS[step])
