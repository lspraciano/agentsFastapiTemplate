from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from configuration.configs import settings

mongo_uri: str = settings.MONGO_URI
async_mongodb_client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_uri)
client_mongo: MongoClient = MongoClient(mongo_uri)
