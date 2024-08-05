from django.contrib import admin
from django.urls import path
from women.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('women/', index),
]
