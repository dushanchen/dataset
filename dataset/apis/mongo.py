from django.conf import settings


from pymongo import MongoClient

host = settings.MONGO_HOST
port = settings.MONGO_PORT


mongo = MongoClient(host=host, port=port)

def insert():
	pass


