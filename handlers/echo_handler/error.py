from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.update import Update
from loader import dp


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_errors_handler(update: Update, exception: MessageNotModified) -> bool:
    """Skipps 'message not modified' errors"""
    return True
