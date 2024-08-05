from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import *

def index(request):
    return HttpResponse("Page not found")

def categories(request, cat_id):
    return HttpResponse(f'<h1>Article on categories</h1><p>id: {cat_id}</p>')

def categories_by_slug(request, cat_slug):
    return HttpResponse(f'<h1>Article on categories</h1><p>slug: {cat_slug}</p>')

def archive(request, year):
    if int(year) > 2024:
        return redirect('home')
    return HttpResponse(f"<h1>Archive for year</h1><p>{year}</p>")
