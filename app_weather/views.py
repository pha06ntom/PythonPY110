from django.shortcuts import render
from django.http import JsonRespose
# Create your views here.

def weather_view(request):
    if request.method == "GET":
        data
