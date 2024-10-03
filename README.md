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

В проекте sitewomen есть следующие приложения: women и users

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

### Что такое Django REST Framework (lesson-1 drf):

Django REST Framework (DRF) — это мощный и гибкий инструмент для создания веб-API на основе фреймворка Django. Он позволяет легко разрабатывать интерфейсы для взаимодействия с данными в формате JSON или других форматах, таких как XML. DRF предоставляет множество готовых решений для сериализации данных, обработки запросов и работы с аутентификацией.

#### Для чего нужен Django REST Framework?

1. **Создание API для обмена данными**  
   DRF позволяет создавать RESTful API, с помощью которых различные приложения (например, мобильные или frontend-приложения) могут взаимодействовать с серверной частью. API служит посредником между клиентом и сервером, обрабатывая запросы клиента (например, получение данных) и возвращая результаты в удобном формате (обычно JSON).
   
   ![Пример работы REST API][alt text]

   [alt text]: https://berkeley-gif.github.io/caladapt-docs/_images/restapi_model.png "Пример работы REST API"  

   <div align = "center">
   </center><b>Пример работы REST API</b></center>
   </div>
   <br>
2. **Сериализация данных**  
   Сериализация — это процесс преобразования данных из объектов модели в формат JSON, который может быть отправлен через API. DRF предоставляет удобные инструменты для автоматической сериализации данных с помощью классов `Serializer` или `ModelSerializer`.

3. **Удобная работа с запросами**  
   Django REST Framework предоставляет классы для обработки различных HTTP-запросов (GET, POST, PUT, DELETE). Эти классы, такие как `APIView` или `ViewSet`, облегчают создание логики взаимодействия с данными через API.

4. **Аутентификация и разрешения**  
   DRF поддерживает множество методов аутентификации, включая токеновую аутентификацию, OAuth, JWT и другие. Это позволяет защищать доступ к API и контролировать права доступа пользователей к данным.

5. **Гибкость и расширяемость**  
   DRF легко интегрируется в существующий проект Django, а также предоставляет широкий набор классов и миксинов, которые можно использовать или расширять для создания более сложной логики работы с API.

### Тестовый пример для API (lesson-2 drf):

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

### Детальный разбор работы представлений (lesson-3 drf):