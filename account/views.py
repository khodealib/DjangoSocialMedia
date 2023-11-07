from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

from account.forms import UserLoginForm, UserRegistrationForm
from account.models import Relation


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "account/register.html"
    redirect_url = "home:index"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            messages.success(request, "User registered successfully.", "success")
            return redirect(self.redirect_url)

        return render(request, self.template_name, {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"
    redirect_url = "home:index"
    next = None

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                messages.success(request, "You logged in successfully.", "success")
                if self.next:
                    return redirect(self.next)
                return redirect(self.redirect_url)
            messages.warning(request, "Username or password is wrong.", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    redirect_url = "home:index"

    def get(self, request):
        logout(request)
        messages.success(request, "You logged out successfully.", "success")
        return redirect(self.redirect_url)


class UserProfileView(LoginRequiredMixin, View):
    template_name = "account/profile.html"

    def get(self, request, user_id: int):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(
            from_user=request.user,
            to_user=user,
        )
        if relation.exists():
            is_following = True
        posts = user.posts.all()
        context = {
            "user": user,
            "posts": posts,
            "is_following": is_following,
        }
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


class UserFollowView(LoginRequiredMixin, View):
    redirect_url = "account:user_profile"

    def get(self, request, user_id: int):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(
            from_user=request.user,
            to_user=user,
        )
        if relation.exists():
            messages.error(request, "You are already following this user.", "danger")
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, "You followed this user.")

        return redirect(self.redirect_url, user.id)


class UserUnFollowView(LoginRequiredMixin, View):
    redirect_url = "account:user_profile"

    def get(self, request, user_id: int):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(
            from_user=request.user,
            to_user=user,
        )
        if relation.exists():
            relation.delete()
            messages.success(request, "You unfollowed this user.", "success")
        else:
            messages.error(request, "You are not following this user.", "danger")

        return redirect(self.redirect_url, user.id)
