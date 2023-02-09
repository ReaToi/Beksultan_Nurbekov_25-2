from django.shortcuts import HttpResponse
from datetime import datetime
# Create your views here.


def hello(request):
    if request.method == 'GET':
        return HttpResponse('Hello! Its my project"')


def now_date(request):
    if request.method == 'GET':
        return HttpResponse(datetime.now())


def goodby(request):
    if request.method == 'GET':
        return HttpResponse('Goodby User!')

