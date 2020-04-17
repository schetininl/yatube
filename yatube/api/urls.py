from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, PostViewSet_v2, CommentViewSet_v2

router = DefaultRouter()
router.register('posts', PostViewSet, basename='user')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename="comment")

router_v2 = DefaultRouter()
router_v2.register('posts', PostViewSet_v2, basename='user')
router_v2.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet_v2, basename="comment")

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
    path('v2/api-token-auth/', views.obtain_auth_token),
    path('v2/', include(router_v2.urls)),
]