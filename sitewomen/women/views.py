from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse

# from django.template.loader import render_to_string

from .models import *

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Контакты", "url_name": "contact"},
    {"title": "Вход", "url_name": "login"},
]

data_db = [
    {
        "id": 1,
        "title": "Актриса 1",
        "content": """<h1>zz</h1> zzz zz zzz z zzzz zzzzz zzz zzz zz zzz zz zz zz z
        zzzzz zzzzz zzz zzz zz zz zz zz zzz zzzzz
        zzzzz zzzzz zzz zzz zz zz zz zz zzz zzzzz
        zzzzz zzzzz zzz zzz zz zz zz zz zzz zzzzz 
        zz zzz zzzz zzzz zzzzz zzz zzzz zzzz z zzz zzz zzz zz zz zzzz zzzzz zzz
        zzzzzzzzzzz""",
        "is_published": True,
    },
    {
        "id": 2,
        "title": "Актриса 2",
        "content": "Биография актрисы 2",
        "is_published": False,
    },
    {
        "id": 3,
        "title": "Актриса 3",
        "content": "Биография актрисы 3",
        "is_published": True,
    },
]


cats_db = [
    {"id": 1, "name": "Актрисы"},
    {"id": 2, "name": "Певицы"},
    {"id": 3, "name": "Спортсменки"},
]


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": data_db,
        "cat_selected": 0,
    }
    return render(request, "women/index.html", context=data)


def about(request):
    return render(request, "women/about.html", {"title": "О сайте", "menu": menu})


def show_post(request, post_id):
    return HttpResponse(f"Showing post with id = {post_id}")


def add_page(request):
    return HttpResponse("Add page")


def contact(request):
    return HttpResponse("Contact")


def login(request):
    return HttpResponse("Login")


def show_category(request, cat_id):
    data = {
        "title": "Отопражение по рубрикам",
        "menu": menu,
        "posts": data_db,
        "cat_selected": cat_id,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
