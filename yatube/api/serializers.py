from rest_framework import serializers
from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)
    group = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)
        
    class Meta:
        model = Comment
        fields = ('id', 'post', 'text', 'author', 'created')