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

### [1. Что такое Django REST Framework](https://rutube.ru/video/ac3445780e670f48ebfe1fd55aab8dd7/?playlist=536685&playlistPage=1)

Django REST Framework (DRF) — это мощный и гибкий инструмент для создания веб-API на основе фреймворка Django. Он позволяет легко разрабатывать интерфейсы для взаимодействия с данными в формате JSON или других форматах, таких как XML. DRF предоставляет множество готовых решений для сериализации данных, обработки запросов и работы с аутентификацией.

#### Для чего нужен Django REST Framework?

1. **Создание API для обмена данными**  
   DRF позволяет создавать RESTful API, с помощью которых различные приложения (например, мобильные или frontend-приложения) могут взаимодействовать с серверной частью. API служит посредником между клиентом и сервером, обрабатывая запросы клиента (например, получение данных) и возвращая результаты в удобном формате (обычно JSON).

   ![Пример работы REST API][alt text]

   [alt text]: https://github.com/user-attachments/assets/2839adff-518f-4936-b371-caf4235d0587 "Пример работы REST API"

   <div align = "center">
   </center><b>Пример работы REST API</b></center>
   </div>
   <br>

2. **Сериализация данных**  
   Сериализация — это процесс преобразования данных из объектов модели в формат JSON, который может быть отправлен через API. DRF предоставляет удобные инструменты для автоматической сериализации данных с помощью классов `Serializer` или `ModelSerializer`.

   ![Пример работы Django REST Framework][alt text 2]

   [alt text 2]: https://github.com/user-attachments/assets/752767db-e5fd-4782-9984-9c00314a07fa "Пример работы Django REST Framework"

   <div align = "center">
   </center><b>Пример работы Django REST Framework</b></center>
   </div>
   <br>

3. **Удобная работа с запросами**  
   Django REST Framework предоставляет классы для обработки различных HTTP-запросов (GET, POST, PUT, DELETE). Эти классы, такие как `APIView` или `ViewSet`, облегчают создание логики взаимодействия с данными через API.

4. **Аутентификация и разрешения**  
   DRF поддерживает множество методов аутентификации, включая токеновую аутентификацию, OAuth, JWT и другие. Это позволяет защищать доступ к API и контролировать права доступа пользователей к данным.

5. **Гибкость и расширяемость**  
   DRF легко интегрируется в существующий проект Django, а также предоставляет широкий набор классов и миксинов, которые можно использовать или расширять для создания более сложной логики работы с API.

### [2. Тестовый пример для API](https://rutube.ru/video/983339116167f2a0f65ba0533523d50d/?playlist=536685&playlistPage=1)

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
      """
      Класс, представляющий API для получения списка женщин.

      Этот класс наследует функционал от класса ListAPIView, что позволяет
      выводить список объектов из модели Women
      Используется для реализации GET-запросов, возвращающих список всех объектов
      модели.

      Атрибуты
      --------
      queryset : QuerySet
         Набор данных, содержащий все объекты модели Women
      serializer_class : Serializer
         Сериализатор, который отвечает за преобразование объектов модели в
         формат JSON

      Методы
      ------
      get(request, *args, **kwargs)
         Метод для обработки GET-запросов и возврата списка женщин. Данный метод
         унаследован от класса ListAPIView
      """
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

### [3. Детальный разбор работы представлений](https://rutube.ru/video/66b47f4203b73f33fcf038709954567d/?playlist=536685&playlistPage=1)

Для начала рассмотрим работу класса представления `WomenAPIView`, обходясь без сериализатора.

#### Выполнение POST и GET-запросов с помощью Postman

Postman - это инструмент для тестирования API, который позволяет легко отправлять запросы и получать ответы от вашего API. Ниже приведен пример того, как можно протестировать простое API с GET и POST-запросами, используя Postman.

Так выглядит простой класс представления, который возвращает данные в ответ на GET и POST-запросы:

```python
from rest_framework.response import Response
from rest_framework.views import APIView

class WomenAPIView(APIView):

   def get(self, request):
      return Response({"title": "Angelina Jolie"})

   def post(self, request):
      return Response({"title": "Jennifer Shrader Lawrence"})
```

#### Шаги для тестирования API, приведенного выше, с помощью Postman:

1. **Запуск сервера Django**  
   Перед тем как тестировать API, убедитесь, что сервер Django запущен. Для этого выполните команду:

   ```bash
   python manage.py runserver
   ```

2. **Отправка GET-запроса**

   Откройте Postman и выберите метод GET.

   Введите URL для вашего API, например:

   `http://127.0.0.1:8000/api/v1/womenlist/`

   Нажмите кнопку Send.

   Ожидаемый результат: Вы получите JSON-ответ:

   ```json
   {
     "title": "Angelina Jolie"
   }
   ```

3. **Отправка POST-запроса**

   В Postman выберите метод POST.

   Введите тот же URL:

   `http://127.0.0.1:8000/api/v1/womenlist/`

   Нажмите кнопку Send.

   Ожидаемый результат: Вы получите JSON-ответ:

   ```json
   {
     "title": "Jennifer Shrader Lawrence"
   }
   ```

#### Модернизация GET и POST-запросов

Видоизменим методы класса. Метод `get` теперь отправляет список всех записей из таблицы `women_women`. Метод `post` - добавляет новый элемент в таблицу `women_women`.

```python
from django.forms import model_to_dict

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women

class WomenAPIView(APIView):
   """
   Этот API возвращает данные о женщинах в ответ на GET и POST-запросы.

   Класс наследует функционал от класса APIView, представляя базовые методы для
    обработки HTTP-запросов (GET, POST и другие). Он позволяет реализовать логику
    для взаимодействия с моделью Women.

   Методы
   ------
   get(self, request)
      Метод для обработки GET-запросов. Возвращает список записей из таблицы women_women.

   post(self, request)
      Метод для обработки POST-запросов. Позволяет добавлять новые записи в таблицу women_women, используя данные в теле запроса. Возвращает данные записи в формате JSON.
   """
   def get(self, request):
      lst = Women.objects.all().values()
      return Response({"posts": list(lst)})

   def post(self, request):
      post_new = Women.objects.create(
         title=request.data["title"],
         content=request.data["content"],
         cat_id=request.data["cat_id"],
      )
      # Исключаем поле с файлом, добавлять файл будем позже с помощью сериализатора
      post_dict = model_to_dict(post_new, exclude=["photo"])
      return Response({"post": post_dict})

```

1. **GET-запрос**  
   Теперь, если выполнить GET-запрос, мы увидим список из соответствующих записей таблицы `women_women`. Важный момент, если бы было записано `lst = Women.objects.all()`, вышла бы ошибка, говорящая о отсутствии сериализации. приписка `.values()` возвращает конкретные значения.

   Ожидаемый результат: вы получите JSON-ответ:

   ```json
   {
      "posts": [
         {
            "id": 15,
            "title": "Эллен Хог",
            "slug": "ellen-hog",
            "photo": "photos/2023/09/13/elen-hog.jpg",
            "content": "Эллен Мартейн Хог (нидерл. Ellen Martijn Hoog; 26 марта 1986, Блумендал, Нидерланды) — бывшая нидерландская хоккеистка на траве, игрок национальной сборной Нидерландов.",
            "time_create": "2023-09-13T08:19:08.042938Z",
            "time_update": "2023-09-13T08:19:08.042938Z",
            "is_published": true,
            "cat_id": 1,
            "husband_id": 1,
            "author_id": null
         },
         ...
         {
            "id": 1,
            ...
         }
      ]
   }
   ```

2. **POST-запрос**  
   Для правильного выполнения POST-запроса, перед нажатием **Send** выполните следующие шаги:

- Перейдите на вкладку **Body**.
- Выберете опцию **raw**.
- Справа от этой опции выберете тип данных как **JSON**.
- Введите данные для отправки в виде JSON.
  Пример:

  ```json
  {
    "title": "Светлана Ходченкова",
    "content": "Светлана Ходченкова - актриса",
    "cat_id": 1
  }
  ```

- Нажимаете кнопку **Send**.

  Ожидаемый результат: вы получите JSON-ответ:

  ```json
  {
    "post": {
      "id": 16,
      "title": "Светлана Ходченкова",
      "slug": "",
      "content": "Светлана Ходченкова - актриса",
      "is_published": 0,
      "cat": 1,
      "husband": null,
      "author": null,
      "tags": []
    }
  }
  ```

  Вместе с JSON-ответом в таблице `women_women` появится новая запись.

#### Заключение по Postman

Postman позволяет легко тестировать API-запросы (GET, POST и другие методы) и получать быстрые ответы от вашего Django REST Framework приложения. Это удобный инструмент для отладки и проверки API без необходимости писать клиентские приложения.

### [4. Введение в сериализацию](https://rutube.ru/video/3049b97773ea79d5b9382b84bb1cde0f/?r=a)

Еще раз повторим, что при реализации API сайта обмен данными реализовон посредством определенного формата: **`.json`** или `.xml`.

Роль сериализатора - выполнять конвертирования произвольных объектов в формат `.json`, в том числе модели Django и queryset, и наоборот, и `json`-формата в соответствующие объекты языка Python.

#### Создание сериалиатора

В serializers.py создадим:
1. **Класс, имитирующий модель Women:**
   ```python
   class WomenModel(): # Имитирование модели Women
      def __init__(self, title, content):
         self.title = title
         self.content = content
   ```
2. **Класс сериализатора:**
   ```python
   from rest_framework import serializers 

   class WomenSerializer(serializers.Serializer):
      title = serializers.CharField(max_length=255)
      content = serializers.CharField()
   ```
   Добавляем переменные в тело класса. Делается для того, чтобы сериализатор знал, что, например, `title` - представляет собой строку.
3. **Функция encode**
   Чтобы увидеть, как взаимодействуют классы WomenModel и WomenSerializer, объявим функцию encode. Она будет преобразовывать объкеты WomenModel в `json`-формат.
   ```python
   from rest_framework.renderers import JSONRenderer

   def encode():
      model = WomenModel("Name", "Name - content")
      model_sr = WomenSerializer(model)
      print(model_sr.data, type(model_sr.data), sep="\n")
      json = JSONRenderer().render(model_sr.data)
      print(json)
   ```
   В этой функции мы объект `model` пропускаем через сериализатор. Следующей строчкой мы передаем `model` в Meta класс класса WomenSerializer. Строкой, где мы присваиваем значение переменной `json`, преобразуется объект сериализации в байтовую `json`-строку.

   Переходим в терминал

   ```bash
   (venv) root@localhost:~/source/django/sitewomen# python3 manage.py shell
   >>> from women.serializers import encode
   >>> encode
   {'title': 'Name', 'content': 'Name - content'}
   <class 'rest_framework.utils.serializers_helpers.ReturnDict'>
   b'{"title": "Name", "content": "Name - content"}'
   ```
   Возвращается первой строкой словарь, второй строкой тип данных переменной словаря `model_sr.data`. Третья строка - байтовая строка.

4. **Функция decode()**
   Осуществим обратное преобразование, преобразование байтовой строки в словарь:
   ```python
   import io
   from rest_framework.parsers import JSONParser
   
   def decode():
      stream = io.BytesIO(b'{"title": "Name", "content": "Name - content"}')
      data = JSONParser().parse(stream)
      serializer = WomenSerializer(data=data) # Используем именованный параметр data= для декодирования
      serializer.is_valid() # Проверяем корректность
      print(serializer.validated_data)
   ```

   Переходим в терминал

   ```bash
   (venv) root@localhost:~/source/django/sitewomen# python3 manage.py shell
   >>> from women.serializers import decode
   >>> decode
   OrderedDict([('title', 'Name'), ('content', 'Name - content')])
   ```
5. **Сериализатор с моделью Women**  
   Применим сериализатор для нашей моедли `Women`. В классе сериализатора пропишем все атрибуты, что есть в нашей модели.

   ```python
   from rest_framework import serializers

   from .models import Women

   class WomenSerializer(serializers.ModelSerializer):
      class Meta:
         model = Women
         fields = [
            "title",
            "slug",
            "photo",
            "content",
            "time_create",
            "time_update",
            "is_published",
            "cat",
            "tags",
            "husband",
            "author",
         ]
   ```
   Переходим в `views.py`:
   ```python
   from rest_framework.response import Response
   from rest_framework.views import APIView

   from .serializers import WomenSerializer

   class WomenAPIView(APIView):

      def get(self, request):
         w = Women.objects.all()
         return Response({"posts": WomenSerializer(w, many=True).data})

      def post(self, request):
         post_new = Women.objects.create(
            title=request.data["title"],
            content=request.data["content"],
            cat_id=request.data["cat_id"],
         )
         post_dict = model_to_dict(post_new, exclude=["photo"])
         return Response({"post": WomenSerializer(post_new).data})
   ```
   С методом post могут возникнуть трудности, так как при отсутствии одного из элементов в PostData (тело post запроса в postman), получим ошибку.

   **Решение проблемы:**
   ```python
      def post(self, request):
         serializer = WomenSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         post_new = Women.objects.create(
            title=request.data["title"],
            slug=request.data["slug"],
            content=request.data["content"],
            cat_id=request.data["cat_id"],
         )
         return Response({"post": WomenSerializer(post_new).data})
   ```
   Здесь мы первой строчкой создаем сериализатор на базе полученных данных с post-запроса, следующей строчкой проверяем корректность, причем в виде json-строки `(raise_exception=True)`. Но так как модель Women имеет больше четырех параметров, то для них элементов в классе `WomenSerializer` надо указать флаг `read_only=True`.
   ```python
   class WomenSerializer(serializers.ModelSerializer):
      """
      Сериализатор для модели Women, используемый для преобразования данных между
      экземплярами модели и JSON-форматом.

      Args:
         serializers (ModelSerializer): Базовый класс для сериализации моделей.
      """
      # Указываем поля, которые дожны быть доступны только для чтения
      time_create = serializers.DateTimeField(read_only=True)
      time_update = serializers.DateTimeField(read_only=True)
      is_published = serializers.BooleanField(read_only=True)
      photo = serializers.ImageField(read_only=True)
      husband = serializers.PrimaryKeyRelatedField(read_only=True)
      author = serializers.PrimaryKeyRelatedField(read_only=True)
      # Решаем проблему с появлением ошибки ManyRelatedManager
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
   ```
   Отправляем следующий POST-запрос:
   ```json
   {
      "title": "Юлия Снегирь",
      "slug": "yulia-snegir",
      "content": "Юлия Снегирь - актриса",
      "cat_id": 1
   }
   ```
   Получим следующий ответ:
   ```json
   {
      "post": {
         "title": "Юлия Снегирь",
         "slug": "yulia-snegir",
         "photo": null,
         "content": "Юлия Снегирь - актриса",
         "time_create": "2024-10-14T15:30:56.004241+03:00",
         "time_update": "2024-10-14T15:30:56.004465+03:00",
         "is_published": false,
         "cat_id": 1,
         "tags": [],
         "husband": null,
         "author": null
      }
   }
   ```
### [5. Методы save(), vreate() и update() класса Serializer](https://rutube.ru/video/92fd842cbb6fe655b971d4dc086610f8/?r=a)
На прошлом занятии сделали сериализатор, который преобразовывает объекты в формат `json` и обратно. По идее, сериализаторы должны сохранять или изменять данные, а также удалять их. Сейчас этот функционал на себя берет ```class WomenAPIView(APIView):```. В этой главе мы поправим это недоразумение!

```python
class WomenSerializer(serializers.ModelSerializer):
   # Добавили title, content, cat_id для контроля их валидации и типов данных
   # Помогает избежать ошибок при post-запросе
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
   
   ... # Тут должен быть метакласс

   def create(self, validated_data):
      return Women.objects.create(**validated_data)
```
```python
class WomenAPIView(APIView):
   ...# Тут должен быть get-запрос
   def post(self, request):
      serializer = WomenSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save() # Вызывает метод create класса WomenSerializer
      return Response({"post": serializer.data}) 
      # Ссылаемся на объект, созданный с помощью метода create
```
```json
{
	"title": "Юлия Снегирь",
	"slug": "yulia-snegir",
	"content": "Юлия Снегирь - актриса",
	"cat_id": 1
}
```


```json
{
  "post": {
    "title": "Юлия Снегирь",
    "slug": "yulia-snegir",
    "photo": null,
    "content": "Юлия Снегирь - актриса",
    "time_create": "2024-10-18T10:29:03.426731+03:00",
    "time_update": "2024-10-18T10:29:03.426911+03:00",
    "is_published": false,
    "cat_id": 1,
    "tags": [],
    "husband": null,
    "author": null
  }
}
```