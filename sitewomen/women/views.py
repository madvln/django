"""
Функции и классы отображения в приложении Women
"""

from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework import generics

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.forms import model_to_dict
from django.core.paginator import Paginator
from django.db import connection

# from django.http import Http404
# from django.shortcuts import redirect
# from django.utils.text import slugify
# from django.urls import reverse
# from django.conf import settings
# from django.views import View

from .forms import AddPostForm
from .models import Women, TagPost
from .utils import DataMixin

# from .models import Category, UploadFiles
from .serializers import WomenSerializer


class WomenAPIView(APIView):
    """Этот API возвращает данные о женщинах в ответ на GET и POST-запросы.

    Класс наследует функционал от класса APIView, представляя базовые методы для
    обработки HTTP-запросов (GET, POST и другие). Он позволяет реализовать логику
    для взаимодействия с моделью Women.

    Methods:
        - get: возвращает список женщин.
        - post: добавляет новую запись о женщине.
    """

    def get(self, request):
        """Метод для обработки GET-запросов. Возвращает фиксированные данные в виде
        JSON строки.

        Args:
            request (Request): HTTP-запрос, содержащий данные, необходимые для создания новой записи

        Returns:
            Response: Ответ с данными записей модели Women в формате JSON.
        """
        w = Women.objects.all()
        return Response({"posts": WomenSerializer(w, many=True).data})

    def post(self, request):
        """Метод для обработки POST-запросов. Позволяет добавлять новые записи в
        таблицу women_women, используя данные в теле запроса. Возвращает данные
        записи в формате JSON.

        В теле запроса должны содержаться поля: title, slug, content, cat_id.
        Остальные поля - необязательны.

        Args:
            request (Request): HTTP-запрос, содержащий данные, необходимые для
            создания новой записи

        Returns:
            Response: Ответ с данными созданной записи в формате JSON.
        """
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() # Вызывает метод create класса WomenSerializer
        # post_new = Women.objects.create(
        #     title=request.data["title"],
        #     slug=request.data["slug"],
        #     content=request.data["content"],
        #     cat_id=request.data["cat_id"],
        # )
        return Response({"post": serializer.data}) # Ссылаемся на объект, 
        # созданный с помощью метода create
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        instance.delete()
        drop_autoincrement()
        return Response({"post": "delete post" + str(pk)})

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

def drop_autoincrement():
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'women_women';"
        )