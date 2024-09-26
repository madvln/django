from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .forms import (
    LoginUserForm,
    RegisterUserForm,
    ProfileUserForm,
    UserPasswordChangeForm,
)
from .models import User


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    # def get_success_url(self):
    #     return reverse_lazy("home")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:register_done")


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {"title": "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "Пользователь с таким email не найден.")
            return self.form_invalid(form)
        return super().form_valid(form)


# def register(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data["password"])
#             user.save()
#             return render(request, "users/register_done.html")
#     else:
#         form = RegisterUserForm()
#     return render(request, "users/register.html", {"form": form})

# def login_user(request):
#     if request.method == "POST":
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                 request, username=cd["username"], password=cd["password"]
#             )
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse("home"))
#     else:
#         form = LoginUserForm()
#     return render(request, "users/login.html", {"form": form})


# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("users:login"))
