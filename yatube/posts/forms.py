from django.db import models
from django.forms import ModelForm, Textarea
from .models import Post, Comment, User

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
            'image': ('Изображение'),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Комментарий'
        }
        widgets = {
            'text': Textarea(attrs={'rows': 3}),
        }

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя*',
            'email': 'Адрес электронной почты'
        }
