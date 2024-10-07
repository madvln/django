from rest_framework import serializers

from .models import Women


class WomenSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для модели Women

    Этот класс используется для преобразования объектов модели Women в формат
    JSON и обратно, что позволяет взаимодействовать с API и базой данных в
    удобном формате.

    Атрибуты
    --------
    Meta : class
        Внутренний класс, определяющий параметры сериализации.

        Атрибуты класса Meta
        --------------------
        model : Model
            Модель, с которой связан данный сериализатор
            (в данном случае Women).
        fields : tuple
            Поля модели, которые будут включены в сериализацию
            (title и cat_id).
    """

    class Meta:
        model = Women
        fields = ("title", "cat_id")
