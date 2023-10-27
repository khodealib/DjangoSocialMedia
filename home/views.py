from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views import View

from home.forms import PostUpdateForm
from home.models import Post


class HomeView(View):
    template_name = "home/index.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        posts = Post.objects.all()
        return render(request, self.template_name, {"posts": posts})


class PostDetailView(View):
    template_name = "home/detail.html"

    def get(self, request: HttpRequest, post_id: int,
            post_slug: str) -> HttpResponse:
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, self.template_name, {"post": post})


class PostDeleteView(LoginRequiredMixin, View):
    redirect_url = "home:index"

    def get(self, request: HttpRequest, post_id) -> HttpResponse:
        post = get_object_or_404(Post, pk=post_id)
        if post.user.pk == request.user.pk:
            post.delete()
            messages.success(request, "Post delete successfully.")
        else:
            messages.error(request, "You can't delete this post.")

        return redirect(self.redirect_url)


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    post_instance = None

    def setup(self, request: HttpRequest, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs.get("post_id"))
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        post = self.post_instance
        if not post.user.pk == request.user.pk:
            messages.error(request, "You can't update this post.")
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, "home/update.html", {"form": form})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, "You updated this post")
            return redirect("home:post_detail", post.pk, post.slug)
