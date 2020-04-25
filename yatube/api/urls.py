from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


router = DefaultRouter()
router.register('posts', PostViewSet, basename='user')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename="comment")
router.register('group', GroupViewSet, basename='group')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/docs/redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
    path('v1/', include(router.urls)),
]
