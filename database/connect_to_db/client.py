from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection

from config_data.config import MONGO_DB_USERNAME, MONGO_DB_PASSWORD

# mongoserver.db = 130.61.88.150 (/etc/hosts)
client = motor_asyncio.AsyncIOMotorClient(f'mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@130.61.88.150'
                                          '/?retryWrites=true&w=majority')
#client = motor_asyncio.AsyncIOMotorClient(f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@hotelscluster.wodas.mongodb.net'
#                                          '/?retryWrites=true&w=majority')


def get_favorites_collection() -> AsyncIOMotorCollection:
    """Returns async collection of favorite hotels from MongoDB"""

    db = client['Hotels']
    return db['Favorites']


def get_history_collection() -> AsyncIOMotorCollection:
    """Returns async collection of user history from MongoDB"""

    db = client['Hotels']
    return db['History']
