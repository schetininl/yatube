from django.db import models
from django.forms import ModelForm, Textarea
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text']
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
        }
        widgets = {
            'text': Textarea(attrs={'cols': 100, 'rows': 15}),
        }