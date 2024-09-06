from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Контакты", "url_name": "contact"},
    {"title": "Вход", "url_name": "login"},
]


class WomenHome(ListView):
    # model = Women
    template_name = "women/index.html"
    context_object_name = "posts"
    extra_context = {
        "title": "Главная страница",
        "menu": menu,
        "cat_selected": 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related("cat")


def about(request):

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()
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


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            "menu": menu,
            "title": "Добавление статьи",
            "form": form,
        }
        return render(request, "women/addpage.html", data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
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


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.select_related("cat")
#     data = {
#         "title": f"Рубрика: {category.name}",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": category.pk,
#     }
#     return render(request, "women/index.html", context=data)


class WomenCategory(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        context["title"] = "Категория - " + cat.name
        context["menu"] = menu 
        context["cat_selected"] = cat.pk 
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class WomenTags(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context["posts"][0].tags.first()
        context["title"] = "Тег - " + tag.tag
        context["menu"] = menu 
        context["cat_selected"] = None
        return context