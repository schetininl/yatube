from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        read_only_fields = ('pub_date', )
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'description', 'rules')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    def validate_author(self, value):
        user = self.context['request'].user
        author = get_object_or_404(User, username=value)
        follow_check = Follow.objects.filter(user=user, author=author).exists()
        if follow_check:
            raise serializers.ValidationError(f"Вы уже подписаны на {author.username}")
        return value

    class Meta:
        fields = ('user', 'author')
        model = Follow