from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = """
#     АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
#     абвгдеёжзийклмнопрстуфхцчшщъыьэюя
#     0123456789- 
#     """
#     code = "russian"

#     def __init__(self, message=None):
#         self.message = (
#             message
#             if message
#             else "Должны присутсвовать только русские символы, дефис и пробел."
#         )

#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)


# class AddPostForm(forms.Form):
#     title = forms.CharField(
#         max_length=255,
#         min_length=5,
#         label="Заголовок:",
#         widget=forms.TextInput(attrs={"class": "form-input"}),
#         # validators=[
#         #     RussianValidator(),
#         # ],
#         error_messages={
#             "min_length": "Слишком короткий заголовок",
#             "required": "Без заголовка никак",
#         },
#     )
#     slug = forms.SlugField(
#         max_length=255,
#         label="URL:",
#         validators=[
#             MinLengthValidator(5, message="Минимум 5 символов"),
#             MaxLengthValidator(100, message="Максимум 100 символов"),
#         ],
#     )
#     content = forms.CharField(
#         widget=forms.Textarea(attrs={"cols": 50, "rows": 5}),
#         required=False,
#         label="Контент:",
#     )
#     is_published = forms.BooleanField(required=False, label="Статус:", initial=True)
#     cat = forms.ModelChoiceField(
#         queryset=Category.objects.all(),
#         label="Категории:",
#         empty_label="Категория не выбрана",
#     )
#     husband = forms.ModelChoiceField(
#         queryset=Husband.objects.all(),
#         required=False,
#         label="Муж:",
#         empty_label="Не замужем",
#     )

#     def clean_title(self):
#         title = self.cleaned_data["title"]
#         ALLOWED_CHARS = """
#         АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
#         абвгдеёжзийклмнопрстуфхцчшщъыьэюя
#         0123456789-
#         """

#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError(
#                 "Должны присутсвовать только русские символы, дефис и пробел."
#             )


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категории",
        empty_label="Категория не выбрана",
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        required=False,
        label="Муж",
        empty_label="Не замужем",
    )

    class Meta:
        model = Women
        fields = [
            "title",
            "slug",
            "content",
            "is_published",
            "cat",
            "husband",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }
        labels = {"slug": "URL"}

    def clean_title(self):
        title = self.cleaned_data["title"]
        ALLOWED_CHARS = """
        АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
        абвгдеёжзийклмнопрстуфхцчшщъыьэюя
        0123456789-
        """

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError(
                "Должны присутсвовать только русские символы, дефис и пробел."
            )

        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title
