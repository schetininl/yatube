from django_filters import rest_framework as filters
from rest_framework import serializers
from posts.models import Post, Comment


class PostFilter(filters.FilterSet):
    date_from = filters.DateTimeFilter(field_name="pub_date", lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name="pub_date", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['author', 'date_from', 'date_to', 'group']


class CommentFilter(filters.FilterSet):
    date_from = filters.DateTimeFilter(field_name="created", lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name="created", lookup_expr='lte')

    class Meta:
        model = Comment
        fields = ['author', 'date_from', 'date_to']