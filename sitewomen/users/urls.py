from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
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
    path(
        "register/done/",
        TemplateView.as_view(template_name="users/register_done.html"),
        name="register_done",
    ),
    # path(
    #     "password-reset/",
    #     PasswordResetView.as_view(template_name="users/password_reset_form.html"),
    #     name="password_reset",
    # ),
    path(
        "password-reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path("profile/", views.ProfileUser.as_view(), name="profile"),
]
