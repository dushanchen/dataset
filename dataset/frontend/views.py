from django.shortcuts import render

# Create your views here.


def index(request):
	ctx = {'menu': 'index'}
	return render(request, 'index.html', ctx)


def product(request):
	ctx = {'menu': 'index'}
	return render(request, 'product.html', ctx)


def personal(request):
	ctx = {'menu': 'personal'}
	return render(request, 'personal.html', ctx)


def map(request):
	ctx = {'menu': 'map'}
	return render(request, 'map.html', ctx)