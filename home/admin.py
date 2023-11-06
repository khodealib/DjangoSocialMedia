from django.contrib import admin

from home.models import Comment, Post, Vote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "slug", "updated")
    search_fields = ("slug", "body")
    list_filter = ("updated",)
    prepopulated_fields = {"slug": ("body",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created", "is_reply")
    list_filter = ("created", "is_reply")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
