from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher

from config_data.config import DEFAULT_COMMANDS


async def set_default_commands(dp: Dispatcher):
    """Initiates default commands from commands list"""

    await dp.bot.set_my_commands(
        [BotCommand(*command_info) for command_info in DEFAULT_COMMANDS]
    )
