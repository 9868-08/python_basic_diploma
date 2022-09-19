from database.connect_to_db.client import get_history_collection


async def is_hotels_were_found(user_id, call_time: str) -> bool:
    """Checks if hotels were found after calling the command"""

    collection = get_history_collection()

    user: dict = await collection.find_one({'_id': user_id})
    history = user['history']
    found_hotels = history[call_time]['found_hotels']

    return True if found_hotels else False
