from django.urls import path

from home import views

app_name = "home"
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path(
        "post/<int:post_id>/<slug:post_slug>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "post/delete/<int:post_id>/", views.PostDeleteView.as_view(), name="post_delete"
    ),
    path(
        "post/update/<int:post_id>/", views.PostUpdateView.as_view(), name="post_update"
    ),
]
