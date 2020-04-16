from django.shortcuts import render, get_object_or_404
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from posts.models import Post, Comment
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated,
        IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
        IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get("post_id"))