from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View

from home.forms import CommentCreateForm, PostCreateUpdateForm
from home.models import Post


class HomeView(View):
    template_name = "home/index.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        posts = Post.objects.all()
        return render(request, self.template_name, {"posts": posts})


class PostDetailView(View):
    form_class = CommentCreateForm
    template_name = "home/detail.html"
    post_instance = None

    def setup(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post_slug = kwargs.get("post_slug")
        self.post_instance = get_object_or_404(
            Post,
            pk=post_id,
            slug=post_slug,
        )
        return super().setup(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(
            request,
            self.template_name,
            {
                "post": self.post_instance,
                "comments": comments,
                "form": self.form_class,
            },
        )

    @method_decorator(login_required)
    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = self.post_instance
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, "Your comment submitted successfully.")
            return redirect(
                "home:post_detail",
                self.post_instance.id,
                self.post_instance.slug,
            )


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
    form_class = PostCreateUpdateForm
    post_instance = None

    def setup(self, request: HttpRequest, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs.get("post_id"))
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
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.save()
            messages.success(request, "You updated this post")
            return redirect("home:post_detail", post.pk, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, "home/create.html", {"form": form})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "You created new post successfully.")
            return redirect("home:post_detail", new_post.pk, new_post.slug)
