from database.connect_to_db.client import get_history_collection


async def clear_history(user_id: int):
    """Clear all user history in db"""

    collection = get_history_collection()
    await collection.update_one({'_id': user_id}, {'$set': {'history': {}}})
