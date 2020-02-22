from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    rules = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group", blank=True, null=True
    )

    def __str__(self):
        return str(self.id)
