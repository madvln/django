from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


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
            "photo",
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


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
