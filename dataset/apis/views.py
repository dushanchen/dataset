from django.shortcuts import render

# Create your views here.


mongo = pymongo.MongoClient('127.0.0.1:27017')
datahub = mongo['shanghai']
schema = mongo['shanghai']['schema']


def index(request):

	items = []
	for i in schema.find():
		items.append(i['item'])
		name = i['name']
		names = i['names']
		fields = i['fields']

		count = datahub[name].count()
		