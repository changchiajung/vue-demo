from django.shortcuts import render
from .models import feed

from django.core import serializers
from django.http import HttpResponse
# Create your views here.


def index(request):
    results = feed.objects.all()
    context = {
        'results': results,
    }
    return render(request,"index.html",context)


def base_layout(request):
    return render(request,"index.html")


def getdata(request):
	results=feed.objects.all()
	jsondata = serializers.serialize('json',results)
	return HttpResponse(jsondata)