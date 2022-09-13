from aiogram.types.callback_query import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from keyboards.inline.bestdeal.select_keyboards import distance_range_keyboard
from states.bot_states import BestDeal, SelectDates
from utils.named_tuples import KM

from utils.work_with_messages.delete_messages import delete_errors_messages
from .select_date import start_select_date_in
from loader import dp


async def start_select_distance_range(call, state):
    """Starts the distance selection process"""

    await state.update_data(max_distance=None)
    await BestDeal.select_distance_range.set()
    await call.message.answer('<b>Укажите максимальную удаленность от центра</b>',
                              reply_markup=distance_range_keyboard())


@dp.callback_query_handler(lambda call: call.data == 'select_max_distance', state=BestDeal.select_distance_range)
async def send_max_distance_request(call: CallbackQuery, state: FSMContext):
    """Asks the user for the maximum distance from the center"""

    await call.message.edit_reply_markup(reply_markup=None)
    message = await call.message.answer('<b>Отправьте максимальную удаленность от центра в Км</b>\n'
                                        'Пример: <b>5</b> или <b>10.5</b>')
    await state.update_data(message_to_delete=message)
    await state.update_data(errors_messages=[])
    await state.update_data(message_to_edit=call.message)
    await BestDeal.wait_max_distance.set()


@dp.message_handler(state=BestDeal.wait_max_distance)
async def get_max_distance(message: Message, state: FSMContext):
    """Gets maximum distance and checks it"""

    state_data = await state.get_data()
    errors: list[Message] = state_data.get('errors_messages')
    try:
        distance: KM = float(message.text)
    except ValueError:
        error_message = await message.answer('<b>❗️Отправьте боту число!</b>')
        errors.extend([error_message, message])
        await state.update_data(errors_messages=errors)
        return

    messsage_from_bot: Message = state_data.get('message_to_delete')
    messsage_from_user: Message = message

    message_with_select_distance: Message = state_data.get('message_to_edit')
    await messsage_from_bot.delete()
    await messsage_from_user.delete()

    await state.update_data(max_distance=distance)
    await delete_errors_messages(message_list=errors)
    await state.update_data(errors_messages=[])
    await edit_distance_message(message_to_edit=message_with_select_distance, state=state)
    await BestDeal.select_distance_range.set()


async def edit_distance_message(message_to_edit: Message, state: FSMContext):
    """Edits message with info about maximum distance"""

    state_data = await state.get_data()
    max_distance = state_data.get('max_distance')

    text = f'<b>Укажите максимальную удаленность от центра</b>\n' \
           f'Максимальное расстояние: <b>{max_distance} Км</b>'

    await message_to_edit.edit_text(text=text, reply_markup=distance_range_keyboard())


@dp.callback_query_handler(lambda call: call.data == 'end_distance_range', state=BestDeal.select_distance_range)
async def end_distance_range_selecting(call: CallbackQuery, state: FSMContext):
    """Ends the distance selecting process"""

    state_data = await state.get_data()

    if state_data.get('max_distance') is None:
        await state.update_data(max_distance=1000)

    await call.message.edit_text('<b>🏠 Диапазон расстояния выбран!</b>')
    await SelectDates.start_select_date_in.set()
    await start_select_date_in(call=call)
