from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views import View

from home.models import Post


class HomeView(View):
    template_name = "home/index.html"

    def get(self, request: HttpRequest):
        posts = Post.objects.all()
        return render(request, self.template_name, {"posts": posts})


class PostDetailView(View):
    template_name = "home/detail.html"

    def get(self, request: HttpRequest, post_id: int, post_slug: str):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, self.template_name, {"post": post})
