from django.urls import path

from account import views

app_name = "account"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path(
        "profile/<int:user_id>/",
        views.UserProfileView.as_view(),
        name="user_profile",
    ),
    path(
        "password/reset/",
        views.UserPasswordResetView.as_view(),
        name="user_password_reset",
    ),
    path(
        "password/reset/done/",
        views.UserPasswordResetDoneView.as_view(),
        name="user_password_reset_done",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>",
        views.UserPasswordResetConfirmView.as_view(),
        name="user_password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        views.UserPasswordResetCompleteView.as_view(),
        name="user_password_reset_complete",
    ),
]
