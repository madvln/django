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
    title = serializers.CharField(max_length=255) 
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    cat_id = serializers.IntegerField()
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

    def create(self, validated_data):
        return Women.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.content = validated_data.get("content", instance.content)
        instance.cat_id = validated_data.get("cat_id", instance.cat_id)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.save()
        return instance


# lesson 4 drf legacy
# class WomenSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для модели Women, используемый для преобразования данных между
#     экземплярами модели и JSON-форматом.

#     Args:
#         serializers (ModelSerializer): Базовый класс для сериализации моделей.
#     """
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(read_only=True)
#     photo = serializers.ImageField(read_only=True)
#     husband = serializers.PrimaryKeyRelatedField(read_only=True)
#     author = serializers.PrimaryKeyRelatedField(read_only=True)
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=TagPost.objects.all(), many=True, required=False
#     )

#     class Meta:
#         """
#         Определяет метаданные для сериализатора WomenSerializer, включая
#         связанную модель и поля, которые будут сериализованы.

#         Attributes:
#             model (Model): Модель, к которой относится данный сериализатор.
#             fields (list): Список полей, которые будут сериализованы.
#         """
#         model = Women
#         fields = [
#             "title",
#             "slug",
#             "photo",
#             "content",
#             "time_create",
#             "time_update",
#             "is_published",
#             "cat_id",
#             "tags",
#             "husband",
#             "author",
#         ]

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
