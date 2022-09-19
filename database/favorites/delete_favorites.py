from database.connect_to_db.client import get_favorites_collection


async def clear_favorites(user_id: int):
    """Clear all hotels entries from user favorites in db"""

    collection = get_favorites_collection()
    await collection.update_one({'_id': user_id}, {'$set': {'favorites': {}}})
