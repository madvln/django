# Django

## Описание

Проект django создан в процессе обучения по видео из канала [selfedu](https://youtu.be/oBU83uojltE?si=c8E9WdSOK2VPuSnN)

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/madvln/django.git
   cd django
   ```

2. **Создайте и активируйте виртуальное окружение:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Установите зависимости:**

   Убедитесь, что ваше виртуальное окружение активно, и выполните команду:

   ```bash
   pip install -r requirements.txt
   ```

4. **Запустите сервер Django:**

   ```bash
   python3 manage.py runserver
   ```

## Проект sitewomen

Здесь будет описан проект sitewomen. Он был создан следующей командой:

```bash
django-admin startproject sitewomen
```

### Приложение women:

Здесь будет описано приложение women. Оно был создано следующей командой:

```bash
python3 manage.py startapp women
```

### Приложение users:

Здесь будет описано приложение users. Оно был создано следующей командой:

```bash
python3 manage.py startapp users
```

## Django REST Framework

В проекте используется Django REST Framework для создания REST API. С помощью этого фреймворка можно взаимодействовать с данными в формате JSON.

### Знакомство с Django REST Framework:

1. **Сериализаторы**
   Классы сериализаторов используются для преобразования объектов моделей в JSON и обратно. В нашем проекте используется `WomenSerializer`, который сериализует поля `title` и `cat_id` модели `Women`.

   ```python
   from rest_framework import serializers

   from .models import Women


   class WomenSerializer(serializers.ModelSerializer):
      class Meta:
         model = Women
         fields = ("title", "cat_id")
   ```

2. **APIView**
   Для обработки запросов на API используется класс WomenAPIView, который наследуется в свою очередь свой функционал от класса ListAPIView. Этот класс автоматически обрабатывает GET-запросы и возвращает список объектов модели Women в формате JSON.

   ```python
   from rest_framework import generics

   from .models import Women
   from .serializers import WomenSerializer


   class WomenAPIView(generics.ListAPIView):
      queryset = Women.objects.all()
      serializer_class = WomenSerializer
   ```

3. **Маршрутизация**
   В проекте добавлен маршрут для доступа к API:

   ```python
   from women.views import WomenAPIView

   urlpatterns = [
      path("api/v1/womenlist/", WomenAPIView.as_view()),
   ]
   ```
