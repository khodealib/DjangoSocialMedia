from django import forms

from home.models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)
