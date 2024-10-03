from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.forms import model_to_dict
from django.core.paginator import Paginator

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddPostForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin
from .serializers import WomenSerializer


# class WomenAPIView_old(generics.ListAPIView):
#     """
#     Класс, представляющий API для получения списка женщин.

#     Этот класс наследует функционал от класса ListAPIView, что позволяет
#     выводить список объектов из модели Women
#     Используется для реализации GET-запросов, возвращающих список всех объектов
#     модели.

#     Атрибуты
#     --------
#     queryset : QuerySet
#         Набор данных, содержащий все объекты модели Women
#     serializer_class : Serializer
#         Сериализатор, который отвечает за преобразование объектов модели в
#         формат JSON

#     Методы
#     ------
#     get(request, *args, **kwargs)
#         Метод для обработки GET-запросов и возврата списка женщин. Данный метод
#         унаследован от класса ListAPIView
#     """

#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


class WomenAPIView(APIView):
    """
    Этот API возвращает данные о женщинах в ответ на GET и POST-запросы.

    Класс наследует функционал от класса APIView, представляя базовые методы для 
    обработки HTTP-запросов (GET, POST и другие). Он позволяет реализовать логику
    для взаимодействия с моделью Women. 

    Методы
    ------
    get(self, request)
        Метод для обработки GET-запросов. Возвращает список записей из таблицы 
        women_women.

        Атрибуты метода get
        -------------------
        lst : ValuesQuerySet
            Переменная, представляющая собой QuerySet, где каждая запись является
            словарём (dict), содержащим пары "поле-значение" для каждой строки 
            модели Women.
    
    post(self, request)
        Метод для обработки POST-запросов. Позволяет добавлять новые записи в 
        таблицу women_women, используя данные в теле запроса. Возвращает данные 
        записи в формате JSON.

        Атрибуты метода post
        --------------------
        post_new : Women
            Экземпляр модели Women. Конкретнее, который создается и сохраняется 
            в базе данных с помощью метода create().
    """

    def get(self, request):
        lst = Women.objects.all().values()
        return Response({"posts": list(lst)})
    
    def post(self, request):
        # Проверяем, передан ли файл для поля photo
        photo = request.data.get("photo", None)
        post_new = Women.objects.create(
            title=request.data["title"],
            content=request.data['content'],
            cat_id=request.data["cat_id"],
            photo=photo if photo else None
        )

        return Response({"post": model_to_dict(post_new)})


class WomenHome(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related("cat")


# @login_required(login_url="/admin/") # 1-й в очереди
@login_required
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "women/about.html",
        {"title": "О сайте", "page_obj": page_obj},
    )


class ShowPost(DataMixin, DetailView):
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    title_page = "Добавление статьи"
    # login_url = "/admin/" # 1-й в очереди
    permission_required = "women.add_women"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"
    permission_required = "women.change_women"


class DeletePage(DataMixin, DeleteView):
    model = Women
    context_object_name = "post"
    template_name = "women/delete_confirm.html"
    success_url = reverse_lazy("home")
    title_page = "Удаление статьи"


@permission_required(perm="women.view_women", raise_exception=True)
def contact(request):
    return HttpResponse("Contact")


def login(request):
    return HttpResponse("Login")


class WomenCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related(
            "cat"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        return self.get_mixin_context(
            context,
            title="Категория - " + cat.name,
            cat_selected=cat.pk,
        )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class TagPostList(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title="Тег - " + tag.tag)

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")
