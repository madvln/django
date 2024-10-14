import io

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Women, TagPost


class WomenSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Women, используемый для преобразования данных между
    экземплярами модели и JSON-форматом.

    Args:
        serializers (ModelSerializer): Базовый класс для сериализации моделей.
    """
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    photo = serializers.ImageField(read_only=True)
    husband = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=TagPost.objects.all(), many=True, required=False
    )

    class Meta:
        """
        Определяет метаданные для сериализатора WomenSerializer, включая
        связанную модель и поля, которые будут сериализованы.

        Attributes:
            model (Model): Модель, к которой относится данный сериализатор.
            fields (list): Список полей, которые будут сериализованы.
        """
        model = Women
        fields = [
            "title",
            "slug",
            "photo",
            "content",
            "time_create",
            "time_update",
            "is_published",
            "cat_id",
            "tags",
            "husband",
            "author",
        ]


def encode():
    """
    Кодирует экземпляр модели Women в формат JSON.

    Создает экземпляр Women с указанными данными, сериализует его с помощью
    WomenSerializer и выводит закодированные данные в формате JSON.

    Returns:
        None
    """
    model = WomenModel("Name", "Name - content")
    model_sr = WomenSerializer(model)
    print(model_sr.data, type(model_sr.data), sep="\n")
    json = JSONRenderer().render(model_sr.data)
    print(json)


def decode():
    """
    Декодирует JSON-данные в экземпляр WomenSerializer.

    Принимает данные в формате JSON, парсит их и валидирует с помощью
    WomenSerializer. Выводит валидированные данные.

    Returns:
        None
    """
    stream = io.BytesIO(b'{"title": "Name", "content": "Name - content"}')
    data = JSONParser().parse(stream)
    serializer = WomenSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)


# legacy serializer from lesson-2 DRF
# class WomenSerializer(serializers.ModelSerializer):
#     """
#     Класс сериализатора для модели Women

#     Этот класс используется для преобразования объектов модели Women в формат
#     JSON и обратно, что позволяет взаимодействовать с API и базой данных в
#     удобном формате.

#     Атрибуты
#     --------
#     Meta : class
#         Внутренний класс, определяющий параметры сериализации.

#         Атрибуты класса Meta
#         --------------------
#         model : Model
#             Модель, с которой связан данный сериализатор
#             (в данном случае Women).
#         fields : tuple
#             Поля модели, которые будут включены в сериализацию
#             (title и cat_id).
#     """

#     class Meta:
#         model = Women
#         fields = ("title", "cat_id")

# class WomenSerializer(serializers.Serializer):

# legacy model from lesson-4 drf
# class WomenModel:
#     """_summary_

#     Класс, объекты которого будут сериализованы (преобразованы в json-строку).
#     Этот класс имитирует работу моделей Django, но является самостоятельным и
#     не связан с базой данных.

#     Методы
#     ------
#     __init__(self, title, content):
#         Инициализатор, создающий объекты класса WomenModel.

#     """

#     def __init__(self, title, content):
#         """Initializer, which is creating objects of WomenModel class.

#         Args:
#             title (str): Title of an object. Passed, when instance was created
#             content (str): Additional information about object
#         """
#         self.title = title
#         self.content = content


# legacy serializer from lesson-4 DRF
# class WomenSerializer(serializers.Serializer):
#     """_summary_

#     Args:
#         serializers (_type_): _description_
#     """

#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
