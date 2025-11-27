from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017/orderdb")

client = MongoClient(MONGO_URL)
db = client.get_default_database()
orders_collection = db["orders"]
