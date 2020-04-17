from django.shortcuts import render, get_object_or_404
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets, status, permissions, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .pagination import StandardResultsSetPagination
from posts.models import Post, Comment
from .permissions import IsOwnerOrReadOnly
from .filters import PostFilter, CommentFilter


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get("post_id"))


class PostViewSet_v2(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    filter_backends = (SearchFilter, filters.DjangoFilterBackend)
    filterset_class = PostFilter
    search_fields = ['text',]
    filterset_fields = ['pub_date',]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet_v2(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = (SearchFilter, filters.DjangoFilterBackend)
    filterset_class = CommentFilter
    search_fields = ['text',]
    filterset_fields = ['pub_date',]
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get("post_id"))