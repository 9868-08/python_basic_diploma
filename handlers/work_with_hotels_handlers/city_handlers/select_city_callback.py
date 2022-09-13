from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

from handlers.work_with_hotels_handlers.search_details_handlers.select_date import start_select_date_in
from handlers.work_with_hotels_handlers.search_details_handlers.select_price_range import start_select_price_range

from states.bot_states import SelectCity, SelectDates
from loader import dp


@dp.callback_query_handler(lambda call: call.data.startswith('search_in_city'), state=SelectCity.select_city)
async def set_city_id(call: CallbackQuery, state: FSMContext):
    """Get city id (destination id) from callback. Starts selecting dates"""

    city_id = call.data.lstrip('search_in_city')
    await state.update_data(city_id=city_id)

    await call.answer('Город выбран', show_alert=False)
    await call.message.edit_text('<b>🏙 Город выбран!</b>', reply_markup=None)

    state_data = await state.get_data()
    command = state_data.get('command_type')

    if command == 'bestdeal':
        await start_select_price_range(call, state=state)
        return

    await SelectDates.start_select_date_in.set()
    await start_select_date_in(call=call)
