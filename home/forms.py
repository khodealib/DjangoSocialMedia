from django import forms

from home.models import Comment, Post


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"class": "form-control"})}
