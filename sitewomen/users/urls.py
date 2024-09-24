from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.views.generic import TemplateView

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="login"),  # "users:login"
    path("logout/", LogoutView.as_view(), name="logout"),  # "users:logout"
    # path("register/", views.register, name="register"),
    path(
        "password-change/", views.UserPasswordChange.as_view(), name="password_change"
    ),
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path(
        "register/done/",
        TemplateView.as_view(template_name="users/register_done.html"),
        name="register_done",
    ),
    path("profile/", views.ProfileUser.as_view(), name="profile"),
]
