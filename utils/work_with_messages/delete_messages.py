from aiogram.types.message import Message, Chat


async def delete_message(message: Message):
    """Deletes message"""

    chat: Chat = message.chat
    message_id: int = message.message_id

    await chat.delete_message(message_id=message_id)


#async def delete_errors_messages(message_list: list[Message]):
async def delete_errors_messages():
    """Deletes messages with errors while user selecting something in bestdeal scenario"""
    pass
'''    if message_list is None:
        return
    for message in message_list:
        await message.delete()
'''