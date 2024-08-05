from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import *

def index(request):
    return HttpResponse("Page not found")
