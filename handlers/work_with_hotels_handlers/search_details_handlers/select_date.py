from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

from datetime import datetime

from states.bot_states import SelectDates, GetHotels
from utils.misc.is_correct_inline import is_correct_markup
from utils.misc.work_with_dates import get_readble_date
from keyboards.inline.date_keyboards.date_keyboards import CustomCalendar, CUSTOM_STEPS, create_calendar
from loader import dp


async def start_select_date_in(call: CallbackQuery):
    """Starts the check-in date selection process"""

    calendar_info = create_calendar()
    await call.message.answer(f'↘️ <b>Укажите {calendar_info.date_type} заезда</b>',
                              reply_markup=calendar_info.calendar)
    await SelectDates.select_date_in.set()


async def start_select_date_out(call: CallbackQuery, date_in: datetime):
    """Starts the check-out date selection process"""

    calendar_info = create_calendar(minimal_date=date_in)
    await call.message.answer(f'↘️ <b>Укажите {calendar_info.date_type} выезда</b>',
                              reply_markup=calendar_info.calendar)
    await SelectDates.select_date_out.set()


@dp.callback_query_handler(state=SelectDates.select_date_in)
async def select_date_in(call: CallbackQuery, state: FSMContext):
    """Process of selection check-in date"""

    result, keyboard, step = CustomCalendar().process(call_data=call.data)
    if not result and keyboard:
        await call.message.edit_text(f'↘️ <b>Укажите {CUSTOM_STEPS[step]} заезда</b>',
                                     reply_markup=keyboard)

    elif result:
        await state.update_data(date_in=result)
        message = get_readble_date(str_date=str(result))
        await call.message.edit_text(f'📅 <b>Выбрано: {message}\n'
                                     f'Все верно?</b>', reply_markup=is_correct_markup('date_in'))
        await SelectDates.is_date_correct.set()


@dp.callback_query_handler(state=SelectDates.select_date_out)
async def select_date_out(call: CallbackQuery, state: FSMContext):
    """Process of selection check-out date"""

    state_data = await state.get_data()
    date_in = state_data.get('date_in')
    result, keyboard, step = CustomCalendar(min_date=date_in).process(call_data=call.data)
    if not result and keyboard:
        await call.message.edit_text(f'↘️ <b>Укажите {CUSTOM_STEPS[step]} выезда</b>',
                                     reply_markup=keyboard)

    elif result:
        await state.update_data(date_out=result)
        message = get_readble_date(str_date=str(result))
        await call.message.edit_text(f'📅 <b>Выбрано: {message}\n'
                                     f'Все верно?</b>', reply_markup=is_correct_markup('date_out'))
        await SelectDates.is_date_correct.set()


@dp.callback_query_handler(state=SelectDates.is_date_correct)
async def send_confirmation_date(call: CallbackQuery, state: FSMContext):
    """
    Gets a response from user about validity of selected date

    Asks user about validity of all received info
    """

    state_data = await state.get_data()
    city = state_data.get('city_name')
    date_in = state_data.get('date_in')
    date_out = state_data.get('date_out')

    if call.data == 'date_in_incorrect':
        await call.answer('Попробуйте еще раз', show_alert=True)
        await call.message.delete()
        await SelectDates.start_select_date_in.set()
        await start_select_date_in(call=call)

    if call.data == 'date_out_incorrect':
        await call.answer('Попробуйте еще раз', show_alert=True)
        await call.message.delete()
        await SelectDates.start_select_date_out.set()
        await start_select_date_out(call=call, date_in=date_in)

    if call.data == 'date_in_correct':
        await call.answer('Укажите дату выезда', show_alert=False)
        await call.message.delete()
        await SelectDates.start_select_date_out.set()
        await start_select_date_out(call=call, date_in=date_in)

    if call.data == 'date_out_correct':
        await call.answer('Дата выезда указана', show_alert=False)
        await call.message.delete()
        await call.message.answer('📅 <b> Дата выбрана!</b>')
        await call.message.answer(f'❓ <b>Город: </b>{city}\n'
                                  f'<b>Дата заезда: </b>{get_readble_date(str(date_in))}\n'
                                  f'<b>Дата выезда: </b>{get_readble_date(str(date_out))}\n'
                                  f'\n'
                                  f'<b>Все верно?</b>', reply_markup=is_correct_markup('city_info'))
        await GetHotels.is_info_correct.set()
