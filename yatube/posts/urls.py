from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_post, name="new_post"),
    path("follow/", views.follow_index, name="follow_index"),
    path("group/<slug>/", views.group_posts, name="group"), 
    path("<username>/", views.profile, name="profile"),
    path("<username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path("<username>/edit/", views.profile_edit, name="profile_edit"),
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("<username>/<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("<username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("<username>/<int:post_id>/comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
]