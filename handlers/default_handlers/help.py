from aiogram.types import Message, CallbackQuery, ContentTypes
from loader import dp

help_text = '<b>Поиск отелей:</b>\n' \
            '/lowprice - Будут найдены отели по возрастанию цены\n' \
            '/highprice - Будут найдены отели по убыванию цены\n' \
            '/bestdeal - Поиск отеля с условиями: диапазон цен, максимальная удаленность от центра\n' \
            '\n<b>Ваши отели:</b>\n' \
            '/history - История поиска. Найденные отели и вызванные команды\n' \
            '/favorites - Отели, добавленные в избранное\n' \
            '\n<b>Стандартные команды</b>\n' \
            '/start - Перезапускает работу бота\n' \
            '/help - Выводит данное сообщение\n' \
            '\n<b>Рекомендации:</b>\n' \
            'При возникших ошибках:\n' \
            '1. Попробуйте перезапустить бота, отправив боту /start\n' \
            '2. Иногда на сервере возникают ошибки, не зависящие от работы бота. Попробуйте запустить бота через ' \
            '1-5 мин\n' \
            '3. Если ошибка сохраняется, Вы всегда можете написать разработчику @dinky_s, приложив скриншот ' \
            'ошибки'

@dp.message_handler(state=None, content_types=ContentTypes.ANY)
async def bot_echo(message: Message):
    """Heandler that takes messages without a filter or state"""
    await message.answer(help_text)
