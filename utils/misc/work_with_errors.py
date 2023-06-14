from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext

from typing import Union

from handlers.default_handlers.start import go_home
from utils.work_with_messages.search_waiting import del_waiting_messages


def is_message_error(message) -> bool:
    """Checks is function returned dictionary with error"""

    if isinstance(message, dict):
        return True
    return False


def create_error_message(error_text: str) -> str:
    """Creates error message by text error from returned dictionary"""
    template = '❗️<b>{}</b>'

    if error_text == 'cities_not_found':
        return template.format('Городов с таким названием не найдено')
    if error_text == 'hotels_not_found':
        return template.format('Отелей с заданными условиями не найдено')
    if error_text == 'favorites_empty':
        return template.format('Список избранного пуст')
    if error_text == 'history_empty':
        return template.format('История пуста')
    if error_text == 'empty':
        return template.format('Произошла ошибка при получении информации о городах. Попробуйте еще раз')
    if error_text == 'timeout':
        return template.format('Произошла ошибка на сервере. Попробуйте еще раз')
    if error_text == 'page_index':
        return template.format('Найденные отели закончились')
    if error_text == 'bad_result':
        return template.format('Возникла ошибка при получении информации. Попробуйте еще раз')


async def finish_with_error(message: Message, state: FSMContext, error: str,
                            to_delete: Union[tuple[Message, Message], Message] = None):
    """Sends to user message about error and ends the scenario"""

    await message.answer(text=create_error_message(error))

    if isinstance(to_delete, Message):
        await to_delete.delete()
    elif isinstance(to_delete, tuple) == 1:
        await del_waiting_messages(*to_delete)

    await go_home(message, state)
