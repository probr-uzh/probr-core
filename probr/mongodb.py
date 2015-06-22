import pymongo
from django.conf import settings

client = pymongo.MongoClient(settings.MONGO_URI)
db = client.get_default_database()

testdb = client.get_database("test")