from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from women.views import page_not_found, WomenAPIView
from sitewomen import settings

urlpatterns = [
    path("admin/", admin.site.urls), 
    # Маршрут для административной панели Django

    path("", include("women.urls")), 
    # Маршрут для приложения women (главная страница)

    path("users/", include("users.urls", namespace="users")), 
    # Маршрут для приложения users, с указанием пространства имен (namespace)
    # Пространство имен используется, чтобы различать одинаковые URL-шаблоны 
    # в разных приложениях

    path("__debug__/", include("debug_toolbar.urls")), 
    # Маршрут для Django Debug Toolbar (инструмент отладки)

    path("api/v1/womenlist/", WomenAPIView.as_view()), 
    # Маршрут для API списка женщин (WomenAPIView)

    path("api/v1/womenlist/<int:pk>/", WomenAPIView.as_view()),
    # Маршрут для API изменения элемента в списке женщин (WomenAPIView)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"
