import os
import uuid
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.conf import settings

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Контакты", "url_name": "contact"},
    {"title": "Вход", "url_name": "login"},
]


def index(request):
    posts = Women.published.all().select_related("cat")
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "cat_selected": 0,
    }
    return render(request, "women/index.html", context=data)


def check_double_name(uploaded_file):
    # Прописываем путь к папке uploads
    upload_dir = os.path.join(settings.BASE_DIR, "uploads")
    # Получаем список файлов
    files = os.listdir(upload_dir)
    # Фильтруем только файлы
    files = [f for f in files if os.path.isfile(os.path.join(upload_dir, f))]
    # Получаем расширение загружаемого файла
    original_extension = os.path.splitext(uploaded_file.name)[1]
    name_file = os.path.splitext(uploaded_file.name)[0]
    # Проверяем, существует ли файл с таким именем
    if uploaded_file.name in files:
        # Генерируем новое имя файла с помощью UUID
        # Имя файла + UUID + .расширение
        uploaded_file.name = f"{name_file}{uuid.uuid4()}{original_extension}"
    return uploaded_file.name


def handle_uploaded_file(f):
    f.name = check_double_name(f)
    with open(
        os.path.join(settings.BASE_DIR, "uploads", f.name), "wb+"
        ) as destination:

        # Грузим файл по частям, так быстрее
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data["file"])
    else:
        form = UploadFileForm()
    return render(
        request,
        "women/about.html",
        {
            "title": "О сайте",
            "menu": menu,
            "form": form,
        },
    )


def show_post(request, post_slug):
    post = Women.published.get(slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }

    return render(request, "women/post.html", data)


def add_page(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            #             print(form.cleaned_data)
            #             try:
            #                 Women.objects.create(**form.cleaned_data)
            #                 return redirect("home")
            #             except:
            #                 form.add_error(None, "Ошибка добавления поста")
            form.save()
            return redirect("home")
    else:
        form = AddPostForm()

    data = {
        "menu": menu,
        "title": "Добавление статьи",
        "form": form,
    }
    return render(request, "women/addpage.html", data)


def contact(request):
    return HttpResponse("Contact")


def login(request):
    return HttpResponse("Login")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.select_related("cat")
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


def show_tags_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,
    }
    return render(request, "women/index.html", context=data)
