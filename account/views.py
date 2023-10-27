from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from account.forms import UserLoginForm, UserRegistrationForm
from home.models import Post


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "account/register.html"
    redirect_url = "home:index"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            messages.success(request, "User registered successfully.")
            return redirect(self.redirect_url)

        return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"
    redirect_url = "home:index"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                messages.success(request, "You logged in successfully.")
                return redirect(self.redirect_url)
            messages.warning(request, "Username or password is wrong.")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    redirect_url = "home:index"

    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        messages.success(request, "You logged out successfully.")
        return redirect(self.redirect_url)


class UserProfileView(LoginRequiredMixin, View):
    template_name = "account/profile.html"

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        context = {"user": user, "posts": posts}
        return render(request, self.template_name, context)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:user_password_reset_done")
    email_template_name = "account/password_reset_email.html"


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:user_password_reset_complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"
