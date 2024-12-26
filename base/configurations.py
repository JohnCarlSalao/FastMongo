from pymongo import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI, server_api = ServerApi('1'))
db = client.testdb

todo_data = db["todo_data"]