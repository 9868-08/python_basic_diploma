from aiogram.types.message import Message


class SendedHistory:
    """
    Class that works with sended history messages
    """

    def __init__(self, history_caption: Message):
        self.history_caption: Message = history_caption
        self.command_messages: list[Message] = list()
        self.found_hotels: dict[str, list[Message]] = dict()

    def add_new_command_message(self, message: Message):
        """Adds new message with command info to sended"""

        self.command_messages.append(message)

    def add_new_found_hotel(self, command_cal_time: str, hotel: Message):
        """Adds hotel message to selected history page"""

        found_hotels_of_command = self.found_hotels.get(command_cal_time)
        if found_hotels_of_command is None:
            self.found_hotels[command_cal_time] = list()
            self.found_hotels[command_cal_time].append(hotel)
            return

        self.found_hotels[command_cal_time].append(hotel)

    async def hide_found_hotels(self, command_cal_time: str):
        """Deletes hotel messages of selected history page"""

        found_hotels: list[Message] = self.found_hotels[command_cal_time]

        for hotel in found_hotels:
            await hotel.delete()
        self.found_hotels[command_cal_time] = list()

    async def delete_all_history_messages(self):
        """Deletes all of history messages"""

        for history_page in self.found_hotels.values():
            for hotel in history_page:
                await hotel.delete()

        for command_message in self.command_messages:
            await command_message.delete()

        await self.history_caption.delete()
